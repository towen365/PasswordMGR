#include <SPI.h>
char charRead;
/*
char plaintext[];
char ciphertext[];
char ciphergrid[][];
char finoutput[];
*/
bool isWaiting = true;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Enter text to encrypt");
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    charRead = tolower(Serial.read());
    Serial.write(charRead);
    Serial.println();
  }
  if (charRead == 'e'){
    encrypt();
  }
  else if (charRead == 'd'){
    decrypt();
  }
}

void encrypt(){
  Serial.println("Enter text to Encrypt");
  while (isWaiting == true){
    if(Serial.available()){
      char plaintext[256] = Serial.read();
      isWaiting = false;
    }
  }
  isWaiting = true;
  Serial.println("Enter a 4 digit cipher");
  while (isWaiting == true){
    if(Serial.available()){
      char ciphertext[4] = Serial.read();
      isWaiting = false;
    }
  }

  Serial.println(plaintext);
  Serial.println(ciphertext);
}

void decrypt(){
  Serial.println("Decrpyt");
}
