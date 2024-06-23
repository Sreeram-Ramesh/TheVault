int ls;
int cs;
int rs;
int lmt1 = 5;
int lmt2 = 3;
int rmt1 = 6;
int rmt2 = 11;
void setup() {
  // put your setup code here, to run once:
  pinMode(lmt1,OUTPUT);
  pinMode(lmt2,OUTPUT);
  pinMode(rmt1,OUTPUT);
  pinMode(rmt2,OUTPUT);
  pinMode(9,INPUT);
  pinMode(10,INPUT);
  pinMode(8,INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
ls = digitalRead(7);
cs = digitalRead(8);
rs = digitalRead(9);
if(ls == LOW && cs == LOW && rs == LOW)
{
 backward();
 delay(200);
 right();
 delay(200);  
}
else if(ls == HIGH && cs == LOW && rs == LOW)
{
  backward();
  delay(200);
  left();
  delay(200);
}
else if(ls == LOW && cs == HIGH && rs == LOW)
{
  backward();
  delay(200);
  right();
  delay(200);
}
else if(ls == LOW && cs == LOW && rs == HIGH)
{
  backward(); 
  delay(200);
  right();
  delay(200);
}
else if(ls == HIGH && cs == HIGH && rs == LOW)
{
  left();
}
else if(ls == LOW && cs == HIGH && rs == HIGH)
{
  right();
}
else if(ls == HIGH && cs == LOW && rs == HIGH)
{
  backward();
  delay(200); 
  right();
  delay(200); 
}
else if(ls == HIGH && cs == HIGH && rs == HIGH)
{ 
  forward();
}
}
void forward()
{
 analogWrite(lmt1,150);
 analogWrite(lmt2,0);
 analogWrite(rmt1,150);
 analogWrite(rmt2,0); 
}
void backward()
{
 analogWrite(lmt1,0);
 analogWrite(lmt2,150);
 analogWrite(rmt1,0);
 analogWrite(rmt2,150); 
}
void right()
{
 analogWrite(lmt1,150);
 analogWrite(lmt2,0);
 analogWrite(rmt1,0);
 analogWrite(rmt2,150);
}
void left()
{
 analogWrite(lmt1,0);
 analogWrite(lmt2,150);
 analogWrite(rmt1,150);
 analogWrite(rmt2,0);
}
void stpright()
{
 analogWrite(lmt1,150);
 analogWrite(lmt2,0);
 analogWrite(rmt1,0);
 analogWrite(rmt2,0);
}
void stpleft()
{
 analogWrite(lmt1,0);
 analogWrite(lmt2,0);
 analogWrite(rmt1,150);
 analogWrite(rmt2,0); 
}
void stp()
{
 digitalWrite(lmt1,LOW);
 digitalWrite(lmt2,LOW);
 digitalWrite(rmt1,LOW);
 digitalWrite(rmt2,LOW); 
}
