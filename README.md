## COMPLEX NETWORKS - POLISH ARTIST NETWORK
### Project Description
This project aims to analyze the social networks of Polish artists available on the Spotify platform. The analysis uses graph theory and tools for complex network analysis, which were learned during the "Complex Networks" course.  

Main objectives of the project:

Constructing a network of connections between artists based on their collaborations (e.g., features, joint albums).
Analyzing the network structure: degree, centrality, cliques, coherence.
Using algorithms for community detection in the network.
Examining the relationship between an artist's popularity and their position in the network.
Technologies and Tools
The project uses the following technologies and tools:

Python: programming language used for data processing and graph analysis.
NetworkX: library for network analysis.
Matplotlib/Seaborn: visualization of results.
Spotify API: retrieving data about artists and their collaborations.
Pyviz: additional graph analysis and visualization.
## Project Structure

```bash
spotify-network-analysis/
├── data/               # Input data
├── results/            # Analysis results
├── src/                # Source code
│   ├── spotify_api.py       # Spotify API handling
│   ├── network_analysis.py  # Graph analysis
│   ├── visualization.py     # Result visualization
├── requirements.txt    # List of dependencies
├── README.md           # Project documentation

