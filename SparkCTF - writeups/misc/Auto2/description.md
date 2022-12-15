The best and inexpensive way to practice car hacking is by running an 
instrumentation cluster simulator.Using ICSim, it’s pretty easy to set up and inexpensive to 
learn CAN-Bus exploitation.

In this task you are provided with a dump file containing data sent to some components of the car simulator.

The flag is composed of 4 parts that composes the full hash value, each part is an action made by the driver(data associated with it's ID).
locking the doors >  turning on the right indicator > pressing the accelerator > turning on left indicator 

Flag format:
SparkCTF{locking doors + right indicator +  accelerator + left indicator}

**please consider the order of actions**


Hint1 : why not installing ICSim on your vm and playing around with it?  
Hint2 : image in the folder, Hint2.png

flag: SparkCTF{27AA5BA13AF674F17B3DAABF6015C4B4CFED06C18583570322930F76EB7EFA0E}

Author : jawh3r20