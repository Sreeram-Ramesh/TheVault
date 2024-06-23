#include<Servo.h>
Servo s1;
int lt1 = 3;
int lt2 = 5;
int rt2 = 6;
int rt1 = 11;
int ir1 = 13;
int x = 0;
int sp = 255;
int trig = 8;
int echo = 9;
long duration;
int distance;


void setup() {
  // put your setup code here, to run once:
pinMode(rt1,OUTPUT);
pinMode(rt2,OUTPUT);
pinMode(lt1,OUTPUT);
pinMode(lt2,OUTPUT);
s1.attach(A0);
Serial.begin(9600);
s1.write(92);
pinMode(echo,INPUT);
pinMode(trig,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
chk_obstacle();
if(distance<16)
{
  stp();
  s1.write(2);
  delay(500);
  chk_obstacle();
  if(distance<16)
  {
    s1.write(92);
    delay(2000);
    stp();
  }
  else
  {
    s1.write(92);
    delay(500);
    right();
    delay(500);
    follow();
  }
}
else
{
  follow();
}
}
void chk_obstacle()
{
 
 digitalWrite(trig,LOW);
 delayMicroseconds(2);
 digitalWrite(trig,HIGH);
 delayMicroseconds(10);
 digitalWrite(trig,LOW);
 delayMicroseconds(2);
 duration=pulseIn(echo,HIGH);
 distance=duration*0.034/2; 
}

void follow()
{
  x = digitalRead(ir1);
  delay(100);
  if(x == HIGH)
  {
    stpright();
  }
  else
  {
    stpleft();
  }
}

void forward()
{
  digitalWrite(rt1,sp);
  digitalWrite(rt2,LOW);
  digitalWrite(lt1,sp);
  digitalWrite(lt2,LOW);
}

void backward()
{
  digitalWrite(rt1,LOW);
  digitalWrite(rt2,sp);
  digitalWrite(lt1,LOW);
  digitalWrite(lt2,sp);
}

void right()
{
  digitalWrite(rt1,LOW);
  digitalWrite(rt2,sp);
  digitalWrite(lt1,sp);
  digitalWrite(lt2,LOW);
}

void left()
{
  digitalWrite(rt1,sp);
  digitalWrite(rt2,LOW);
  digitalWrite(lt1,LOW);
  digitalWrite(lt2,sp);
}

void stpright()
{
  digitalWrite(rt1,LOW);
  digitalWrite(rt2,1);
  digitalWrite(lt1,225);
  digitalWrite(lt2,LOW);
}

void stpleft()
{
  digitalWrite(rt1,sp);
  digitalWrite(rt2,LOW);
  digitalWrite(lt1,LOW);
  digitalWrite(lt2,LOW);
}

void stp()
{
  digitalWrite(rt1,LOW);
  digitalWrite(rt2,LOW);
  digitalWrite(lt1,LOW);
  digitalWrite(lt2,LOW);
}
