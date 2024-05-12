# Computing-for-graphics-and-animation

This project constructs a particle system that emits a sphere in an environment that simulates real-world gravity, elasticity, and friction. Users can adjust the color of particles, the elasticity coefficient of the ground and sphere, the time interval between each release of the sphere, and the number of spheres released each time. The size of the sphere and the direction of release are both random.

Run main to run, you need to first install pyopengl, numpy, and glfw.

Initial research: I decided to make a particle launcher that emits small balls to simulate physical properties in reality. And there is a ground that can carry these small balls. I began to think about the physical factors that would affect ball movement. There is gravity, elasticity, and friction. Then I searched for the formulas for these physical phenomena. Gravity formula, friction formula, and elasticity formula.


https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation
https://en.wikipedia.org/wiki/Friction
https://en.wikipedia.org/wiki/Elasticity_(physics)

Next is which language and graphics library should I use. I ultimately used Python because I am quite familiar with it. And I used pyopengl, glfw, and tkiner. Tkinter to create GUI, glfw to create Windows.

Iteration
I first implemented the function of sliding the left mouse button to change the perspective and ground, and then added the function of launching a small ball. I set the parameter of velocity, calculated the velocity based on the launch time and gravitational acceleration, and then calculated the position of the ball to simulate gravity. Next, I determine whether the ball is in contact with the ground by measuring its distance from the ground. If it is in contact, I change the velocity direction to a negative value to simulate the elasticity.

Then I made a GUI for users to input the required ground elasticity, ball elasticity, ball color, firing frequency, and number of balls fired each time. Because the color data output by the GUI is different from the acceptable color data in the main function, I also wrote a colortranslate function to convert the 'FFFFFF' form of color data into (1, 1, 1) form.

Because the color data output by the GUI is different from the acceptable color data in the main function, I also wrote a colortranslate function to convert the 'FFFFFF' form of color data into (1, 1, 1) form.
In order to make the code more concise and clear, I have put the GUI functionality in one file, the particle emission in the emitter file, and the physics file containing simulation physics functionality and scene setting functionality. Finally, run the entire program by running main.


