#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <fcntl.h>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include <utility>
#include <vector>

struct Range {
    std::uint32_t lower;
    std::uint32_t upper;
};

class Oracle {
public:
    Oracle(std::size_t cells, std::uint32_t width) : width_(width) {
        while (capacity_ < cells) capacity_ *= 2;
        lower_.assign(2 * capacity_, std::numeric_limits<std::uint32_t>::max());
        upper_.assign(2 * capacity_, 0);
    }

    void insert(std::size_t cell, Range range) {
        if (cell != initialized_) throw std::runtime_error("out-of-order cell");
        ++initialized_;
        auto position = capacity_ + cell;
        lower_[position] = range.lower;
        upper_[position] = range.upper;
        while (position > 1) {
            position /= 2;
            lower_[position] = std::min(lower_[2 * position], lower_[2 * position + 1]);
            upper_[position] = std::max(upper_[2 * position], upper_[2 * position + 1]);
        }
    }

    Range query(std::uint32_t first, std::uint32_t last) const {
        if (first > last) throw std::runtime_error("empty query");
        if (last / width_ >= initialized_)
            throw std::runtime_error("query includes an uninitialized cell");
        auto left = capacity_ + first / width_;
        auto right = capacity_ + last / width_ + 1;
        Range result {std::numeric_limits<std::uint32_t>::max(), 0};
        while (left < right) {
            if (left % 2) {
                result.lower = std::min(result.lower, lower_[left]);
                result.upper = std::max(result.upper, upper_[left++]);
            }
            if (right % 2) {
                --right;
                result.lower = std::min(result.lower, lower_[right]);
                result.upper = std::max(result.upper, upper_[right]);
            }
            left /= 2;
            right /= 2;
        }
        if (result.lower == std::numeric_limits<std::uint32_t>::max())
            throw std::runtime_error("uninitialized query");
        return result;
    }

    Range cell(std::size_t index) const {
        if (index >= initialized_) throw std::runtime_error("uninitialized cell");
        return {lower_[capacity_ + index], upper_[capacity_ + index]};
    }

private:
    std::size_t capacity_ = 1;
    std::size_t initialized_ = 0;
    std::uint32_t width_;
    std::vector<std::uint32_t> lower_, upper_;
};

std::uint32_t golden(std::uint32_t index) {
    const auto shifted = std::uint64_t(index) + 1;
    const auto radicand = 5 * shifted * shifted;
    auto root = std::uint64_t(std::sqrt(static_cast<long double>(radicand)));
    while ((root + 1) * (root + 1) <= radicand) ++root;
    while (root * root > radicand) --root;
    return (root - shifted) / 2;
}

int generate_values(std::uint32_t limit, const std::string& output, bool visited) {
    if (limit < 4096 || limit >= (std::uint64_t(1) << 31))
        throw std::runtime_error("prefix limit outside supported range");
    std::vector<std::uint32_t> values(limit + 1), selected(4097);
    std::vector<std::uint32_t> stamps(visited ? limit + 1 : 0),
        ranks(visited ? limit + 1 : 0);
    values[1] = values[2] = 1;
    for (std::uint32_t source = 3; source <= limit; ++source) {
        const auto depth = values[source - 1];
        auto next = [&](std::uint32_t point) {
            if (point == 0 || point >= source || values[point] == 0)
                throw std::runtime_error("illegal prefix argument");
            return source - values[point];
        };
        std::uint32_t split = source - 1;
        if (visited) {
            std::uint32_t rank = 0;
            while (stamps[split] != source && rank < depth) {
                stamps[split] = source;
                ranks[split] = rank;
                split = next(split);
                ++rank;
            }
            if (rank < depth) {
                const auto period = rank - ranks[split];
                const auto remaining = (depth - rank) % period;
                for (std::uint32_t step = 0; step < remaining; ++step) split = next(split);
            }
        } else {
            std::uint32_t tortoise = source - 1, hare = next(tortoise);
            std::uint32_t power = 1, period = 1, steps = 1;
            while (hare != tortoise && steps < depth) {
                if (power == period) {
                    tortoise = hare;
                    power *= 2;
                    period = 0;
                }
                hare = next(hare);
                ++period;
                ++steps;
            }
            if (hare == tortoise) {
                const auto remaining = (depth - steps) % period;
                for (std::uint32_t rank = 0; rank < remaining; ++rank) hare = next(hare);
            }
            split = hare;
        }
        values[source] = values[split] + values[source - split];
        if (source <= 4096) selected[source] = split;
    }
    std::vector<std::uint32_t> literal(4097);
    literal[1] = literal[2] = 1;
    for (std::uint32_t source = 3; source <= 4096; ++source) {
        auto point = source - 1;
        for (std::uint32_t rank = 0; rank < literal[source - 1]; ++rank)
            point = source - literal[point];
        literal[source] = literal[point] + literal[source - point];
        if (literal[source] != values[source] || point != selected[source])
            throw std::runtime_error("literal prefix disagreement");
    }
    std::ofstream stream(output, std::ios::binary);
    stream.write(reinterpret_cast<const char*>(values.data()),
                 values.size() * sizeof(std::uint32_t));
    if (!stream) throw std::runtime_error("prefix output failed");
    std::cout << "{\"limit\":" << limit << ",\"literal_check_through\":4096,"
              << "\"selector\":\"" << (visited ? "visited" : "Brent") << "\","
              << "\"format\":\"little-endian uint32, including unused index zero\"}\n";
    return 0;
}

int main(int argc, char** argv) {
    const std::uint32_t byte_order = 1;
    if (*reinterpret_cast<const unsigned char*>(&byte_order) != 1)
        throw std::runtime_error("this binary format requires a little-endian host");
    if ((argc == 4 || argc == 5) && std::string(argv[1]) == "--generate-values") {
        const bool visited = argc == 5;
        if (visited && std::string(argv[4]) != "--visited")
            throw std::runtime_error("unknown generation option");
        return generate_values(std::strtoul(argv[2], nullptr, 10), argv[3], visited);
    }
    if (argc < 3 || argc > 5)
        throw std::runtime_error("expected values path, width, optional certificate and terminal order");
    const std::uint32_t width = std::strtoul(argv[2], nullptr, 10);
    if (width < 16 || width > 65536) throw std::runtime_error("invalid width");
    const int descriptor = open(argv[1], O_RDONLY);
    struct stat information {};
    if (descriptor < 0 || fstat(descriptor, &information) != 0)
        throw std::runtime_error("file unavailable");
    const auto bytes = static_cast<std::size_t>(information.st_size);
    if (bytes % sizeof(std::uint32_t))
        throw std::runtime_error("prefix file size is not a multiple of four");
    const auto* values = static_cast<const std::uint32_t*>(
        mmap(nullptr, bytes, PROT_READ, MAP_PRIVATE, descriptor, 0));
    if (values == MAP_FAILED) throw std::runtime_error("mmap failed");
    const auto retained_cells = (bytes / sizeof(*values)) / width;
    const auto first_unknown = retained_cells * width;
    const auto terminal_order = argc == 5 ? std::strtoul(argv[4], nullptr, 10) : 42;
    if (terminal_order != 42 && terminal_order != 46)
        throw std::runtime_error("terminal order must be42 or46");
    const bool continuation = terminal_order == 46;
    std::vector<std::uint32_t> fibonacci {0, 1};
    while (fibonacci.size() <= 46) fibonacci.push_back(
        fibonacci.back() + fibonacci[fibonacci.size() - 2]);
    if (first_unknown < fibonacci[40] || first_unknown > fibonacci[41])
        throw std::runtime_error("known prefix must end between Fibonacci orders40 and41");
    if (argc >= 4 && std::filesystem::exists(argv[3]) &&
        std::filesystem::equivalent(argv[1], argv[3]))
        throw std::runtime_error("certificate output must differ from the input prefix");
    const auto end = fibonacci[terminal_order] - 1;
    Oracle bounds(std::size_t(end) / width + 1, width);
    for (std::size_t cell = 0; cell < retained_cells; ++cell) {
        Range range {std::numeric_limits<std::uint32_t>::max(), 0};
        for (std::size_t index = cell * width; index < (cell + 1) * width; ++index) {
            range.lower = std::min(range.lower, values[index]);
            range.upper = std::max(range.upper, values[index]);
        }
        bounds.insert(cell, range);
    }
    auto order_of = [&](std::uint32_t index) {
        return std::upper_bound(fibonacci.begin(), fibonacci.end(), index)
            - fibonacci.begin() - 1;
    };
    auto cycle_lower = [&](std::uint32_t index) {
        const auto order = order_of(index);
        return std::max(fibonacci[order - 1], index - fibonacci[order - 1]);
    };
    auto cycle_upper = [&](std::uint32_t index) {
        const auto order = order_of(index);
        return std::min(fibonacci[order], index - fibonacci[order - 2]);
    };
    std::uint32_t maximum_iterations = 0, maximum_readout_cells = 0;
    std::uint64_t total_iterations = 0, total_readout_cells = 0;
    std::uint32_t maximum_numerator = 0, maximum_denominator = 1;
    std::uint32_t contact_cells = 0;
    std::vector<std::pair<std::uint32_t, std::uint32_t>> row_bounds(terminal_order, {0, 1});
    constexpr std::uint64_t numerator = 42085100, denominator = 64203827;
    for (std::size_t cell = retained_cells; cell * width <= end; ++cell) {
        const auto first = std::uint32_t(cell * width);
        const auto last = std::min(std::uint32_t((cell + 1) * width - 1), end);
        auto left = std::max(cycle_lower(first), std::uint32_t(5ULL * first / 9 + 1));
        auto right = std::min(cycle_upper(last), std::uint32_t((2ULL * last - 1) / 3));
        std::uint32_t iterations = 0;
        for (; iterations < 100; ++iterations) {
            if (right / width >= cell) throw std::runtime_error("future orbit query");
            const auto range = bounds.query(left, right);
            const auto next_left = std::max(left, first - range.upper);
            const auto next_right = std::min(right, last - range.lower);
            if (next_left > next_right) throw std::runtime_error("lost all cycles");
            if (next_left == left && next_right == right) break;
            left = next_left;
            right = next_right;
        }
        maximum_iterations = std::max(maximum_iterations, iterations);
        total_iterations += iterations;
        Range readout {std::numeric_limits<std::uint32_t>::max(), 0};
        std::uint32_t readout_cells = 0;
        for (auto argument_cell = left / width; argument_cell <= right / width;
             ++argument_cell) {
            const auto argument_first = std::max(left, argument_cell * width);
            const auto argument_last = std::min(right, (argument_cell + 1) * width - 1);
            const auto argument = bounds.query(argument_first, argument_last);
            const auto complement = bounds.query(first - argument_last, last - argument_first);
            readout.lower = std::min(readout.lower, argument.lower + complement.lower);
            readout.upper = std::max(readout.upper, argument.upper + complement.upper);
            ++readout_cells;
        }
        maximum_readout_cells = std::max(maximum_readout_cells, readout_cells);
        total_readout_cells += readout_cells;
        const auto last_order = order_of(last);
        readout.lower = std::max(readout.lower, golden(first));
        const auto scalar_cap = continuation && first >= fibonacci[41]
            ? std::uint32_t(static_cast<unsigned __int128>(19580084505646265ULL)
                            * last / 29872542956223744ULL)
            : std::uint32_t(numerator * last / denominator);
        readout.upper = std::min(readout.upper, scalar_cap);
        readout.upper = std::min(readout.upper,
            std::min(last - fibonacci[last_order - 2], fibonacci[last_order]));
        if (readout.lower > readout.upper) throw std::runtime_error("inconsistent bound");
        bounds.insert(cell, readout);
        if (last >= fibonacci[41] && first < fibonacci[42]) {
            const auto source_first = std::max(first, fibonacci[41]);
            if (denominator * readout.upper >= numerator * source_first) ++contact_cells;
            if (std::uint64_t(readout.upper) * maximum_denominator >
                std::uint64_t(maximum_numerator) * source_first) {
                maximum_numerator = readout.upper;
                maximum_denominator = source_first;
            }
        }
        const auto first_order = std::max(decltype(last_order)(41), order_of(first));
        for (auto order = first_order; order <= last_order; ++order) {
            const auto source_first = std::max(first, fibonacci[order]);
            auto& maximum = row_bounds[order];
            if (std::uint64_t(readout.upper) * maximum.second >
                std::uint64_t(maximum.first) * source_first)
                maximum = {readout.upper, source_first};
        }
    }
    std::cout << "{\"cell_width\":" << width
              << ",\"known_prefix_through\":" << first_unknown - 1
              << ",\"derived_through\":" << end
              << ",\"max_iterations\":" << maximum_iterations
              << ",\"total_iterations\":" << total_iterations
              << ",\"max_readout_cells\":" << maximum_readout_cells
              << ",\"total_readout_cells\":" << total_readout_cells
              << ",\"row41_contact_cells\":" << contact_cells
              << ",\"row41_bound\":[" << maximum_numerator << ','
              << maximum_denominator << "]";
    if (continuation) {
        std::cout << ",\"row_bounds\":{";
        for (std::size_t order = 41; order < terminal_order; ++order) {
            if (order != 41) std::cout << ',';
            std::cout << '\"' << order << "\":[" << row_bounds[order].first
                      << ',' << row_bounds[order].second << ']';
        }
        std::cout << '}';
    }
    std::cout << "}\n";
    if (argc >= 4) {
        std::ofstream certificate(argv[3], std::ios::binary);
        if (!certificate) throw std::runtime_error("certificate output unavailable");
        const std::uint32_t header[] = {width, std::uint32_t(first_unknown - 1), end};
        certificate.write(reinterpret_cast<const char*>(header), sizeof(header));
        for (std::size_t cell = 0; cell <= end / width; ++cell) {
            const auto range = bounds.cell(cell);
            const std::uint32_t endpoints[] = {range.lower, range.upper};
            certificate.write(reinterpret_cast<const char*>(endpoints), sizeof(endpoints));
        }
        if (!certificate) throw std::runtime_error("certificate output failed");
    }
    munmap(const_cast<std::uint32_t*>(values), bytes);
    close(descriptor);
}
