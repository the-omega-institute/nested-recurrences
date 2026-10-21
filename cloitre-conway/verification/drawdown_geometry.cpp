#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

int main(int argc, char** argv) {
    if (argc > 3 || (argc == 3 && std::string(argv[2]) != "--visited")) throw std::runtime_error("Usage: drawdown_geometry LIMIT [--visited]");
    const unsigned long requested_limit = argc > 1 ? std::strtoul(argv[1], nullptr, 10) : 131072;
    if (requested_limit < 4096 || requested_limit >= (uint64_t(1) << 31)) throw std::runtime_error("Limit must be in [4096, 2^31)");
    const uint32_t limit = requested_limit;
    const bool visited = argc == 3;
    std::vector<uint32_t> values(limit + 1), stamps(visited ? limit + 1 : 0), ranks(visited ? limit + 1 : 0);
    std::vector<uint32_t> trajectory, selected_small(4097), fibonacci{0, 1};
    while (fibonacci.back() <= limit) fibonacci.push_back(fibonacci.back() + fibonacci[fibonacci.size() - 2]);
    values[1] = values[2] = 1;
    uint32_t drawdown = 0, complement_drawdown = 0, maximum_value = 1, maximum_complement = 1;
    uint32_t dual_excess = 0, dual_one_excess = 0, bound_failures = 0, first_bound_failure = 0;
    uint32_t maximum_rise = 0, maximum_record_jump = 0;
    uint32_t even_run = 0, maximum_even = 0, even_end = 0;
    uint32_t core_even_run = 0, maximum_core_even = 0, core_even_end = 0;
    uint32_t negative_run = 0, maximum_negative = 0, negative_end = 0;
    uint32_t strong_run = 0, maximum_strong = 0, strong_end = 0;
    size_t block = 3;
    struct Witness { uint32_t index, value, split; };
    std::vector<Witness> witness;
    for (uint32_t index = 3; index <= limit; ++index) {
        const uint32_t depth = values[index - 1];
        auto next_point = [&](uint32_t point) {
            if (point == 0 || point >= index || values[point] == 0 || values[point] >= index) throw std::runtime_error("Illegal recurrence argument");
            return index - values[point];
        };
        uint32_t split;
        if (visited) {
            trajectory.clear();
            uint32_t point = index - 1;
            while (stamps[point] != index) {
                stamps[point] = index;
                ranks[point] = trajectory.size();
                trajectory.push_back(point);
                point = next_point(point);
            }
            const uint32_t transient = ranks[point], period = trajectory.size() - transient;
            const uint32_t rank = depth < trajectory.size() ? depth : transient + (depth - transient) % period;
            split = trajectory[rank];
            if (index >= 47 && depth < transient) throw std::runtime_error("Selected rank is not cyclic");
        } else {
            uint32_t tortoise = index - 1, hare = next_point(tortoise);
            uint32_t power = 1, period = 1, steps = 1;
            while (hare != tortoise && steps < depth) {
                if (power == period) { tortoise = hare; power *= 2; period = 0; }
                hare = next_point(hare);
                ++period;
                ++steps;
            }
            if (hare == tortoise) {
                const uint32_t remaining = (depth - steps) % period;
                for (uint32_t extra = 0; extra < remaining; ++extra) hare = next_point(hare);
            }
            split = hare;
        }
        values[index] = values[split] + values[index - split];
        if (index <= 4096) selected_small[index] = split;
        drawdown = std::max(drawdown, maximum_value > values[index] ? maximum_value - values[index] : 0);
        const uint32_t complement = index - values[index];
        complement_drawdown = std::max(complement_drawdown, maximum_complement > complement ? maximum_complement - complement : 0);
        maximum_complement = std::max(maximum_complement, complement);
        dual_excess = std::max(dual_excess, complement_drawdown > 2 * drawdown ? complement_drawdown - 2 * drawdown : 0);
        dual_one_excess = std::max(dual_one_excess, complement_drawdown > drawdown ? complement_drawdown - drawdown : 0);
        if (complement_drawdown > 2 * drawdown + 1) {
            ++bound_failures;
            if (!first_bound_failure) first_bound_failure = index + 1;
        }
        maximum_record_jump = std::max(maximum_record_jump, values[index] > maximum_value ? values[index] - maximum_value : 0);
        maximum_value = std::max(maximum_value, values[index]);
        maximum_rise = std::max(maximum_rise, values[index] > values[index - 1] ? values[index] - values[index - 1] : 0);
        even_run = values[index] % 2 == 0 ? even_run + 1 : 0;
        if (even_run > maximum_even) { maximum_even = even_run; even_end = index; }
        while (fibonacci[block + 1] <= index) ++block;
        const bool in_core = uint64_t(10) * (index - fibonacci[block]) >= fibonacci[block - 1]
                             && uint64_t(10) * (fibonacci[block + 1] - index) >= fibonacci[block - 1];
        core_even_run = in_core && values[index] % 2 == 0 ? core_even_run + 1 : 0;
        if (core_even_run > maximum_core_even) { maximum_core_even = core_even_run; core_even_end = index; }
        const int64_t jump = int64_t(index) - values[split] - split;
        negative_run = jump < 0 ? negative_run + 1 : 0;
        if (negative_run > maximum_negative) { maximum_negative = negative_run; negative_end = index; }
        strong_run = 1000 * jump <= -int64_t(index) ? strong_run + 1 : 0;
        if (strong_run > maximum_strong) { maximum_strong = strong_run; strong_end = index; }
        if (index >= 102244566 && index <= 102245060) witness.push_back({index, values[index], split});
    }
    std::vector<uint32_t> literal(4097);
    literal[1] = literal[2] = 1;
    for (uint32_t index = 3; index <= 4096; ++index) {
        uint32_t point = index - 1;
        for (uint32_t step = 0; step < literal[index - 1]; ++step) point = index - literal[point];
        literal[index] = literal[point] + literal[index - point];
        if (literal[index] != values[index] || point != selected_small[index]) throw std::runtime_error("Literal disagreement");
    }
    std::cout << "{\"limit\":" << limit << ",\"literal_check_through\":4096,\"Q\":" << drawdown
              << ",\"complement_Q\":" << complement_drawdown << ",\"max_complement_Q_minus_2Q\":" << dual_excess
              << ",\"max_complement_Q_minus_Q\":" << dual_one_excess << ",\"conjecture_failures\":" << bound_failures
              << ",\"first_failure_N\":" << first_bound_failure << ",\"maximum_rise\":" << maximum_rise
              << ",\"maximum_record_jump\":" << maximum_record_jump
              << ",\"max_even\":" << maximum_even << ",\"even_end\":" << even_end
              << ",\"core_even_max\":" << maximum_core_even << ",\"core_even_end\":" << core_even_end
              << ",\"max_negative\":" << maximum_negative << ",\"negative_end\":" << negative_end
              << ",\"max_strong_negative\":" << maximum_strong << ",\"strong_end\":" << strong_end << ",\"even_witness\":[";
    bool first = true;
    for (const Witness& row : witness) {
        if (!first) std::cout << ",";
        first = false;
        std::cout << "[" << row.index << "," << row.value << "," << row.split << "]";
    }
    std::cout << "]}\n";
}
