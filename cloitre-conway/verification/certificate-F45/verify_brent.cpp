// Independent full evaluation using Brent cycle detection and the prescribed depth.
// This is adapted from the previously checked canonical_erosion evaluator.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
int main(int argc,char**argv) {
 uint32_t limit=argc>1?std::stoul(argv[1]):1134903170;
 if(limit<4096||limit>1134903170) throw std::runtime_error("bad limit");
 const uint32_t lo=433494437, hi=1134903170;
 std::vector<uint32_t> values(size_t(limit)+1),selected(4097);
 std::vector<uint32_t> F{0,1};while(F.back()<=limit)F.push_back(F.back()+F[F.size()-2]);
 uint32_t bnum[60]{},bden[60]{},snum[32]{},sden[32]{},sg[32]{},st[32]{};
 uint32_t maximum_index=0,maximum_value=0;
 uint64_t certificate_indices=0,certificate_failures=0,certificate_equalities=0;
 values[1]=values[2]=1;
 auto started=std::chrono::steady_clock::now();
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
        if (index <= 4096) selected[index] = hare;
        values[index] = values[hare] + values[index - hare];
        if (index >= lo && index < hi) {
            ++certificate_indices;
            if (uint64_t(561724478) * values[index] > uint64_t(367631381) * index) ++certificate_failures;
            if (uint64_t(561724478) * values[index] == uint64_t(367631381) * index) ++certificate_equalities;
            if (maximum_index == 0 || uint64_t(values[index]) * maximum_index > uint64_t(maximum_value) * index) {
                maximum_index = index; maximum_value = values[index];
            }
        }
        unsigned block = 0;
        while (F[block + 1] <= index) ++block;
        if (bden[block] == 0 || uint64_t(values[index])*bden[block] > uint64_t(bnum[block])*index) {
            bden[block]=index; bnum[block]=values[index];
        }
        if (index < (1u<<28)) {
            uint32_t successor=next_point(hare), negative=hare>successor?hare-successor:0;
            unsigned shell=31-__builtin_clz(index);
            if (sden[shell]==0 || uint64_t(negative)*sden[shell]>uint64_t(snum[shell])*index) {
                sden[shell]=index; snum[shell]=negative; sg[shell]=hare; st[shell]=successor;
            }
        }
        if ((index & ((1u<<24)-1))==0) {
            std::cerr << "computed " << index << " / " << limit << " in "
                      << std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count() << " s\n";
        }
    }
    std::vector<uint32_t> literal(4097);
    literal[1]=literal[2]=1;
    for(uint32_t n=3;n<=4096;++n){
        uint32_t x=n-1;
        for(uint32_t j=0;j<literal[n-1];++j)x=n-literal[x];
        literal[n]=literal[x]+literal[n-x];
        if(literal[n]!=values[n]||x!=selected[n])throw std::runtime_error("literal disagreement");
    }
    uint64_t hash=14695981039346656037ull;
    for(uint32_t v:values)for(unsigned j=0;j<4;++j){hash^=(v>>(8*j))&255;hash*=1099511628211ull;}
    std::cout << "{\"method\":\"independent Brent evaluation\",\"limit\":" << limit
              << ",\"literal_check_through\":4096,\"certificate_lo\":" << lo
              << ",\"certificate_hi_exclusive\":" << hi << ",\"certificate_indices\":" << certificate_indices
              << ",\"violations\":" << certificate_failures << ",\"equalities\":" << certificate_equalities
              << ",\"maximum_index\":" << maximum_index << ",\"maximum_value\":" << maximum_value
              << ",\"fnv1a64_le_u32\":\"" << std::hex << hash << std::dec << "\",\"blocks\":[";
    bool first=true;
    for(unsigned k=20;k+1<F.size()&&F[k+1]-1<=limit;++k){
        if(!first)std::cout<<",";first=false;
        std::cout<<"{\"k\":"<<k<<",\"n\":"<<bden[k]<<",\"C\":"<<bnum[k]<<"}";
    }
    std::cout<<"],\"shells\":[";first=true;
    for(unsigned k=3;k<28;++k)if(sden[k]&&((1u<<(k+1))-1)<=limit){
        if(!first)std::cout<<",";first=false;
        std::cout<<"{\"m\":"<<k<<",\"n\":"<<sden[k]<<",\"e_minus\":"<<snum[k]<<",\"g\":"<<sg[k]<<",\"Tg\":"<<st[k]<<"}";
    }
    std::cout<<"]}\n";
    if(argc>2){std::ofstream out(argv[2],std::ios::binary);out.write(reinterpret_cast<char*>(values.data()),values.size()*sizeof(uint32_t));if(!out)throw std::runtime_error("dump failed");}
    return certificate_failures?1:0;
}
