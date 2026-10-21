#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

int main(int argc, char** argv) {
    const unsigned long requested_limit = argc > 1 ? std::strtoul(argv[1], nullptr, 10) : 1048576;
    if (requested_limit < 4096 || requested_limit >= (uint64_t(1) << 31)) throw std::runtime_error("Limit must be in [4096, 2^31)");
    if (argc > 3 || (argc == 3 && std::string(argv[2]) != "--certificate")) throw std::runtime_error("Usage: canonical_erosion LIMIT [--certificate]");
    const uint32_t limit = requested_limit;
    const bool certificate_only = argc == 3;
    std::vector<uint32_t> values(limit + 1), selected(certificate_only ? 4097 : limit + 1);
    uint32_t maximum_index = 0, maximum_value = 0;
    uint64_t certificate_indices = 0, certificate_failures = 0;
    values[1] = values[2] = 1;
    for (uint32_t index = 3; index <= limit; ++index) {
        const uint32_t depth = values[index - 1];
        auto next_point = [&](uint32_t point) {
            if (point == 0 || point >= index || values[point] == 0 || values[point] >= index) throw std::runtime_error("Illegal recurrence argument");
            return index - values[point];
        };
        uint32_t tortoise = index - 1;
        uint32_t hare = next_point(tortoise);
        uint32_t power = 1, period = 1, steps = 1;
        while (hare != tortoise && steps < depth) {
            if (power == period) {
                tortoise = hare;
                power *= 2;
                period = 0;
            }
            hare = next_point(hare);
            ++period;
            ++steps;
        }
        if (hare == tortoise) {
            const uint32_t remaining = (depth - steps) % period;
            for (uint32_t extra = 0; extra < remaining; ++extra) hare = next_point(hare);
        }
        if (!certificate_only || index <= 4096) selected[index] = hare;
        values[index] = values[hare] + values[index - hare];
        if (index >= 102334155 && index < 267914296) {
            ++certificate_indices;
            if (uint64_t(64203827) * values[index] > uint64_t(42085100) * index) ++certificate_failures;
            if (maximum_index == 0 || uint64_t(values[index]) * maximum_index > uint64_t(maximum_value) * index) {
                maximum_index = index;
                maximum_value = values[index];
            }
        }
    }
    std::vector<uint32_t> literal(4097);
    literal[1] = literal[2] = 1;
    for (uint32_t index = 3; index <= std::min(limit, uint32_t(4096)); ++index) {
        uint32_t point = index - 1;
        for (uint32_t step = 0; step < literal[index - 1]; ++step) point = index - literal[point];
        literal[index] = literal[point] + literal[index - point];
        if (literal[index] != values[index] || point != selected[index]) throw std::runtime_error("Literal disagreement");
    }
    if (certificate_only) {
        std::cout << "{\"limit\":" << limit << ",\"method\":\"Independent Brent cycle skipping with exact prescribed depth, no author-generated array\",\"literal_check_through\":4096,\"certificate_indices\":" << certificate_indices << ",\"certificate_failures\":" << certificate_failures << ",\"maximum_index\":" << maximum_index << ",\"maximum_value\":" << maximum_value << "}\n";
        return certificate_failures == 0 ? 0 : 1;
    }
    std::vector<uint32_t> fibonacci{0, 1};
    while (fibonacci.back() <= limit) fibonacci.push_back(fibonacci.back() + fibonacci[fibonacci.size() - 2]);
    std::vector<uint32_t> frontier(fibonacci.size());
    uint64_t total_contacts = 0, non_two_contacts = 0, non_contact_cycle_points = 0;
    uint32_t first_non_two_parent = 0, first_non_contact_parent = 0;
    std::cout << "{\"limit\":" << limit << ",\"literal_check_through\":" << std::min(limit, uint32_t(4096)) << ",\"levels\":[";
    bool first = true;
    for (size_t level = 8; level + 1 < fibonacci.size(); ++level) {
        const uint32_t anchor = fibonacci[level], upper_offset = fibonacci[level - 2];
        if (anchor + upper_offset > limit) break;
        uint32_t count = 0;
        for (uint32_t offset = 1; offset <= upper_offset; ++offset) {
            const uint32_t parent = anchor + offset;
            if (values[parent] != fibonacci[level - 1] + offset) continue;
            ++count;
            ++total_contacts;
            frontier[level] = offset;
            uint32_t cycle_length = 0;
            uint32_t point = selected[parent];
            do {
                const int64_t child_offset = int64_t(point) - fibonacci[level - 1];
                if (int64_t(values[point]) != int64_t(fibonacci[level - 2]) + child_offset) {
                    ++non_contact_cycle_points;
                    if (!first_non_contact_parent) first_non_contact_parent = parent;
                }
                point = parent - values[point];
                if (++cycle_length >= parent) throw std::runtime_error("Selected point is not cyclic");
            } while (point != selected[parent]);
            if (cycle_length != 2) {
                ++non_two_contacts;
                if (!first_non_two_parent) first_non_two_parent = parent;
            }
        }
        const uint32_t offset = frontier[level], parent = anchor + offset;
        const uint32_t split = selected[parent] - fibonacci[level - 1];
        uint32_t cycle_length = 0, point = selected[parent];
        do {
            point = parent - values[point];
            if (++cycle_length >= parent) throw std::runtime_error("Frontier point is not cyclic");
        } while (point != selected[parent]);
        if (!first) std::cout << ",";
        first = false;
        std::cout << "{\"k\":" << level << ",\"tstar\":" << offset << ",\"contacts\":" << count << ",\"s\":" << split << ",\"period\":" << cycle_length;
        if (level >= 10) std::cout << ",\"slack\":" << int64_t(frontier[level - 1]) + frontier[level - 2] - offset << ",\"denominator\":" << frontier[level - 1] + frontier[level - 2];
        std::cout << "}";
    }
    std::cout << "],\"total_positive_contacts\":" << total_contacts << ",\"contacts_with_period_other_than_two\":" << non_two_contacts << ",\"first_non_two_parent\":" << first_non_two_parent << ",\"non_contact_cycle_points\":" << non_contact_cycle_points << ",\"first_non_contact_parent\":" << first_non_contact_parent << ",\"witnesses\":[";
    bool first_witness = true;
    for (uint32_t parent : {uint32_t(29053), uint32_t(122805)}) {
        if (parent > limit) continue;
        if (!first_witness) std::cout << ",";
        first_witness = false;
        size_t level = 2;
        while (fibonacci[level + 1] <= parent) ++level;
        uint32_t literal_point = parent - 1;
        for (uint32_t step = 0; step < values[parent - 1]; ++step) literal_point = parent - values[literal_point];
        if (literal_point != selected[parent]) throw std::runtime_error("Witness orbit disagreement");
        std::cout << "{\"n\":" << parent << ",\"k\":" << level << ",\"offset\":" << parent - fibonacci[level] << ",\"C\":" << values[parent] << ",\"depth\":" << values[parent - 1] << ",\"g\":" << selected[parent] << ",\"cycle\":[";
        uint32_t point = selected[parent];
        bool first_point = true;
        do {
            if (!first_point) std::cout << ",";
            first_point = false;
            const int64_t child_offset = int64_t(point) - fibonacci[level - 1];
            std::cout << "{\"x\":" << point << ",\"C\":" << values[point] << ",\"offset\":" << child_offset << ",\"E\":" << int64_t(fibonacci[level - 2]) + child_offset - values[point] << "}";
            point = parent - values[point];
        } while (point != selected[parent]);
        std::cout << "]}";
    }
    std::cout << "]}\n";
}
