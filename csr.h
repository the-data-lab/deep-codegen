#pragma once

class graph_t {
    public:
        void init_graph();
        void save_graph(const string& full_path);
        void load_graph(const string& full_path);
        void load_graph_noeid(const string& full_path) {
        int get_vcount();
        int get_ecount();
};
