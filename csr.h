#pragma once

#include <string>

using std::string;
typedef uint32_t vid_t;

class graph_t {
public:
    void init(vid_t a_vcount, vid_t a_dstsize, void* a_offset, void* a_nebrs, 
              void* a_offset1, void* a_nebrs1, int64_t a_flag, vid_t edge_count) {};
    void save_graph(const string& full_path) {};
    void load_graph(const string& full_path) {};
    void load_graph_noeid(const string& full_path) {};
    int get_vcount() {return 0;};
    int get_ecount() {return 0;};
};
