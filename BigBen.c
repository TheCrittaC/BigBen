#include <stdio.h> //for printf and scanf
#include <time.h> //for the time things
#include <unistd.h> //for sleep
#include <string.h> //for the string comparison functions
int getHour(){
  time_t rawtime;
  struct tm *timeinfo;
  time(&rawtime);
  timeinfo= gmtime(&rawtime); /*converts the current time into GMT time 
					so Big Ben chimes just as he would in
					London.*/
  return timeinfo->tm_hour % 12; //This way, we get a maximum of 12 BONGs
}

int main(){
  int i;
  int currentHour = getHour(); //sets the current hour so we can monitor it for changes
  char input[5];
  int equal;
  while (0 == 0){
    scanf("%s", &input);
    equal = strcmp(input, ".time");
    if (equal == 0)
      printf("OI IT'S %d BONG\n", getHour());
    if (currentHour != getHour()){
      currentHour = getHour(); //changes the hour so we don't repeat the BONG
      for (i = 0; i < getHour(); i++)
	printf("BONG ");
      printf("\n");
    }
  }
  
  return 0;
  
}

