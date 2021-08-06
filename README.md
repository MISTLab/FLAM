# DORA-Mesh

To compile C++ controller:

- cd /DORA-Mesh/src/controller
- mkdir build
- cd build/ 
- cmake ../src
- make 
- sudo make install

To run the experiment:

- Compile the Buzz script: `make`
- Launch `argos3 -c dora-mesh.argos`
