/*
 *  dht.c:
 *	read temperature and humidity from DHT11 or DHT22 sensor
 */
 
#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
 
#define MAX_TIMINGS	85
#define DHT_PIN		7	/* GPIO-22 */
#include "string.h"
#include "MQTTClient.h"
 
int data[5] = { 0, 0, 0, 0, 0 };
#define ADDRESS     "tcp://localhost:1883"
#define CLIENTID    "HelmetSensors"
#define TOPIC       "helmet/temp"
#define TOPIC2      "helmet/humid"
#define QOS         1
#define TIMEOUT     10000L

// Converts a floating point number to string.
void ftoa(float n, char *res, int afterpoint)
{
    // Extract integer part
    int ipart = (int)n;
 
    // Extract floating part
    float fpart = n - (float)ipart;
 
    // convert integer part to string
    int i = intToStr(ipart, res, 0);
 
    // check for display option after point
    if (afterpoint != 0)
    {
        res[i] = '.';  // add dot
 
        // Get the value of fraction part upto given no.
        // of points after dot. The third parameter is needed
        // to handle cases like 233.007
        fpart = fpart * pow(10, afterpoint);
 
        intToStr((int)fpart, res + i + 1, afterpoint);
    }
}
 
int main( void )
{
	printf( "Raspberry Pi DHT11/DHT22 temperature/humidity test\n" );
 
	if ( wiringPiSetup() == -1 )
		exit( 1 );
/* Connecting MQTT */
    MQTTClient client;
    MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer;
    MQTTClient_message pubmsg = MQTTClient_message_initializer;
    MQTTClient_deliveryToken token;
    int rc;

    MQTTClient_create(&client, ADDRESS, CLIENTID,
        MQTTCLIENT_PERSISTENCE_NONE, NULL);
    conn_opts.keepAliveInterval = 20;
    conn_opts.cleansession = 1;

    if ((rc = MQTTClient_connect(client, &conn_opts)) != MQTTCLIENT_SUCCESS)
    {
        printf("Failed to connect, return code %d\n", rc);
        exit(-1);
}
      char temp[10];
      char humidity[10];

       */ This is the general loop /*
 
	while ( 1 )
	{
	uint8_t laststate	= HIGH;
	uint8_t counter		= 0;
	uint8_t j			= 0, i;
 
	data[0] = data[1] = data[2] = data[3] = data[4] = 0;
 
	/* pull pin down for 18 milliseconds */
	pinMode( DHT_PIN, OUTPUT );
	digitalWrite( DHT_PIN, LOW );
	delay( 18 );
 
	/* prepare to read the pin */
	pinMode( DHT_PIN, INPUT );
 
	/* detect change and read data */
	for ( i = 0; i < MAX_TIMINGS; i++ )
	{
		counter = 0;
		while ( digitalRead( DHT_PIN ) == laststate )
		{
			counter++;
			delayMicroseconds( 1 );
			if ( counter == 255 )
			{
				break;
			}
		}
		laststate = digitalRead( DHT_PIN );
 
		if ( counter == 255 )
			break;
 
		/* ignore first 3 transitions */
		if ( (i >= 4) && (i % 2 == 0) )
		{
			/* shove each bit into the storage bytes */
			data[j / 8] <<= 1;
			if ( counter > 16 )
				data[j / 8] |= 1;
			j++;
		}
	}
 
	/*
	 * check we read 40 bits (8bit x 5 ) + verify checksum in the last byte
	 * print it out if data is good
	 */
	if ( (j >= 40) &&
	     (data[4] == ( (data[0] + data[1] + data[2] + data[3]) & 0xFF) ) )
	{
		float h = (float)((data[0] << 8) + data[1]) / 10;
		if ( h > 100 )
		{
			h = data[0];	// for DHT11
		}
		float c = (float)(((data[2] & 0x7F) << 8) + data[3]) / 10;
		if ( c > 125 )
		{
			c = data[2];	// for DHT11
		}
		if ( data[2] & 0x80 )
		{
			c = -c;
		}
		float f = c * 1.8f + 32;
		printf( "Humidity = %.1f %% Temperature = %.1f *C (%.1f *F)\n", h, c, f );
                ftoa(c, temp, 2);
                ftoa(h, humidity, 2);
                pubmsg.payload = temp;
                pubmsg.payloadlen = strlen(temp);
		pubmsg.qos = QOS;
       		pubmsg.retained = 0;
                MQTTClient_publishMessage(client, TOPIC, &pubmsg, &token);
    		printf("Waiting for up to %d seconds for publication of %s\n"
                	"on topic %s for client with ClientID: %s\n",
                	(int)(TIMEOUT/1000), temp, TOPIC, CLIENTID);
          	rc = MQTTClient_waitForCompletion(client, token, TIMEOUT);
		printf("Message with delivery token %d delivered\n", token);
                pubmsg.payload = humidity;
                pubmsg.payloadlen = strlen(humidity);
		pubmsg.qos = QOS;
       		pubmsg.retained = 0;
                MQTTClient_publishMessage(client, TOPIC2, &pubmsg, &token);
    		printf("Waiting for up to %d seconds for publication of %s\n"
                	"on topic %s for client with ClientID: %s\n",
                	(int)(TIMEOUT/1000), humidity, TOPIC2, CLIENTID);
          	rc = MQTTClient_waitForCompletion(client, token, TIMEOUT);
		printf("Message with delivery token %d delivered\n", token);
		MQTTClient_disconnect(client, 10000);
    		MQTTClient_destroy(&client);
                         
	}else  {
		printf( "Data not good, skip\n" );
	}
 
		delay( 10000 ); /* wait 10 seconds before next read */
	}
 
	return(0);
}
