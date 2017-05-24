#include "lwtnn/LightweightGraph.hh"
#include "lwtnn/parse_json.hh"

#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <cmath>

// For vertex inputs we have an outer map (of input nodes) and an
// inner map (of keyed values)
typedef std::map<std::string, std::map<std::string, double> > input_t;

// For tracks the inputs are similar, but each input node gets a map
// of vectors. The vectors must all be the same length.
typedef std::map<std::string, std::vector<double> > map_vec_t;
typedef std::map<std::string, map_vec_t> inputv_t;

// function ot get dummy values for the vertices
input_t get_vertex_map() {
  return {
    {"vertices", {
        {"sv1_mass", 1},
        {"sv1_sig", 1},
        {"sv1_dr", 1},
        {"jf_mass", 1},
        {"jf_sig", 1},
        {"jf_dr", 1},
        {"who_cares", 1},
        {"bad_variable_name", 1} }
    }
  };
}

// function to get dummy values for the tracks
inputv_t get_track_map() {
  return {
    {"tracks", {
        {"d0", {1,1}},
        {"z0", {1,1}},
        {"ptfrac", {1,1}},
        {"dr", {1,1}} }
    }
  };
}

int main(int argc, char* argv[]) {
  if (argc <= 1) {
    puts("point me to the saved lwtnn network");
    exit(1);
  }
  using namespace lwt;
  std::ifstream input(argv[1]);
  // The graph object initializes from a GraphConfig object
  // since there are multiple outputs for this graph, we have to specify
  // the 'default' value.
  LightweightGraph graph(parse_json_graph(input), "flavor");

  // grab some dummy inputs
  auto tracks = get_track_map();
  auto vertices = get_vertex_map();

  // compute the output for the "default" output, in this case
  // "flavor"
  auto flavmap = graph.compute(vertices, tracks);
  // print out the results
  for (const auto& flav: flavmap) {
    std::cout << flav.first << " " << flav.second << std::endl;
  }

  // print out the charge
  // note the third argument to `compute` which selects the output node
  std::cout << "charge "
            << graph.compute(vertices, tracks, "charge").at("charge")
            << std::endl;
  return 0;
}
