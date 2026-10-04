#include <AccelStepper.h>       //add in the necessary libraries to run stepper motors
#include <MultiStepper.h>

const int motor_step1 = 8;
const int motor_dir1 = 7;
const int motor_step2 = 12;  //making a definition for the pins so code is more readable
const int motor_dir2 = 13;


AccelStepper stepper1(AccelStepper::DRIVER, motor_step1, motor_dir1);   //defining the steppers according to the accell stepper library
AccelStepper stepper2(AccelStepper::DRIVER, motor_step2, motor_dir2);   //Driver has two parameters it looks like.


void setup() {
  // put your setup code here, to run once:
  stepper1.setMaxSpeed(1000);  //steps per second
  stepper1.setAcceleration(8000);

  stepper2.setMaxSpeed(1000);
  stepper2.setAcceleration(8000);

  //defining the pins as output pins and not input pins
  pinMode(motor_step1, OUTPUT);
  pinMode(motor_dir1, OUTPUT);
  pinMode(motor_step2, OUTPUT);
  pinMode(motor_dir2, OUTPUT);

  Serial.begin(9600);  // For debugging purposes this enables the serial monitor 
  Serial.println("Press any key and hit ENTER to start...");

  while (Serial.available() == 0) {
    // Wait here until the user enters something in the Serial Monitor
  }

   //move stepper 1 (shoulder) to the position specified
   stepper1.moveTo(-1892); //multiplied by four to account for microstepping -473 without microstepping

   //move stepper 2(elbow) to the position specified
   stepper2.moveTo(-816);  //multiplied by four to account for microstepping -204 without microstepping

    while (stepper1.isRunning() || stepper2.isRunning()) {
     //This while loops ensures that both motors finish their moves completely before starting the next step
      stepper1.run();
      stepper2.run();
    }

     stepper1.setCurrentPosition(0);
     stepper2.setCurrentPosition(0);


  Serial.println("Starting program...");
}



void loop() {
  if (Serial.available() > 0) {
        String data = Serial.readStringUntil('\n');  // Read incoming data
        int commaIndex = data.indexOf(',');          // Find separator
        
        if (commaIndex != -1) {
            int steps1 = data.substring(0, commaIndex).toInt();  // First value
            int steps2 = data.substring(commaIndex + 1).toInt(); // Second value

            // Move motors
            stepper1.moveTo(steps1);
            stepper2.moveTo(steps2);
            
            while (stepper1.isRunning() || stepper2.isRunning()) {
                stepper1.run();
                stepper2.run();
            }

            Serial.println("Done");  // Send completion message to Python
        }
    }
}
