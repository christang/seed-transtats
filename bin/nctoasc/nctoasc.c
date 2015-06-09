/*   Program nctoasc.c

     Input -- netcdf file - CONUS or Puerto Rico
     Output -- arcview-ready text file

     USAGE:  "nctoasc YYYYMMDD". */


/* change these as needed */
#define INPUT_DIR  "."	/* change this to match your directory structure, or set to "." if the netCDFs are in the same folder as the executable */
#define OUTPUT_DIR "."	/* change this to match your directory structure, or set to "." if you want the text files in the same folder as the executable */
#define LOCATION 1		/* 1 for "CONUS" netCDF file, or 0 for "Puerto Rico" netCDF file */

/*DON'T CHANGE ANYTHING FROM THIS POINT ON */
#if LOCATION==1
  #define	HRAP_X   1051
  #define	HRAP_Y   813
  #define	HRAP_XOR 14
  #define	HRAP_YOR 10
  #define LOCTYPE "conus"
#else
  #define	HRAP_X   110
  #define	HRAP_Y   90
  #define	HRAP_XOR 1480
  #define	HRAP_YOR 142
  #define LOCTYPE "pr"
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <malloc/malloc.h>
#include <math.h>
#include <netcdf.h>

typedef struct _HRAP {
	double x;
	double y;
	} HRAP;

HRAP HrapToLatLong(HRAP hrap)
{
  double raddeg = 57.29577951;
  double earthrad = 6371.2;
  double stdlon = 105.;
  double mesh_len = 4.7625;
  double tlat, rr, gi, ang, x, y;
  HRAP ll;

 tlat=60./raddeg;

 x = hrap.x - 401.;
 y = hrap.y - 1601.;
 rr = x*x + y*y;
 gi = ((earthrad * (1+sin(tlat)))/mesh_len);
 gi=gi*gi;
 ll.y = asin((gi-rr)/(gi+rr))*raddeg;
 ang = atan2(y,x)*raddeg;
 if (ang < 0) ang=ang+360.;
 ll.x = 270+stdlon-ang;
 if (ll.x < 0) ll.x=ll.x+360;
 if (ll.x > 360) ll.x=ll.x-360;
 return ll;
}

int main (int argc, char *argv [])
{
int		i, j, counter;
char 	   	inputdate[11];
FILE		*out_file;
char		infile[150], outfile[150];
int		ncid, hrap_xor_id, hrap_yor_id, hrapx_id, hrapy_id, amountofprecip_id; /*netCDF stuff*/
const size_t	start[] = {0,0}; /*netCDF stuff*/
const size_t	count[] = {HRAP_Y, HRAP_X}; /*netCDF stuff*/
float		xoryor;
int		l_xor, l_yor, l_hrap_x, l_hrap_y;
short int	preciparray[HRAP_Y][HRAP_X];
int			ipreciparray[HRAP_Y][HRAP_X];
HRAP		hrap, latlon;
double		value;
size_t len;
nc_type	preciptype;


if (argc == 2) sprintf(inputdate, "%s", argv[1]);
else  {
   printf ("USAGE: nctoasc YYYYMMDD\n");
   return 1;
   }

/**  open netcdf  **/
sprintf(infile, "%s/nws_precip_%s_%s.nc", INPUT_DIR, LOCTYPE, inputdate);
if (nc_open(infile,0,&ncid) != NC_NOERR)			{ printf("Error could not open %s!\n",infile); return 1; }

/* get dimensions and origin */
if (nc_inq_dimid(ncid,"hrapx",&hrapx_id) != NC_NOERR)		{ printf("Error nc_inq_dimid for hrapx!\n"); return 1; }
if (nc_inq_dimlen(ncid,hrapx_id,&len) != NC_NOERR)		{ printf("Error nc_inq_dimlen for hrapx!\n"); return 1; }
l_hrap_x = (int)len;

if (nc_inq_dimid(ncid,"hrapy",&hrapy_id) != NC_NOERR)		{ printf("Error nc_inq_dimid for hrapy!\n"); return 1; }
if (nc_inq_dimlen(ncid,hrapy_id,&len) != NC_NOERR)		{ printf("Error nc_inq_dimlen for hrapy!\n"); return 1; }
l_hrap_y = (int)len;

if (nc_inq_varid(ncid,"hrap_xor",&hrap_xor_id) != NC_NOERR)	{ printf("Error nc_inq_varid for hrap_xor!\n"); return 1; }
if (nc_get_var1_float(ncid,hrap_xor_id,0,&xoryor) != NC_NOERR)	{ printf("Error nc_get_var1_float for hrap_xor!\n"); return 1; }
l_xor = (int)xoryor;

if (nc_inq_varid(ncid,"hrap_yor",&hrap_yor_id) != NC_NOERR)	{ printf("Error nc_inq_varid for hrap_yor!\n"); return 1; }
if (nc_get_var1_float(ncid,hrap_yor_id,0,&xoryor) != NC_NOERR)	{ printf("Error nc_get_var1_float for hrap_yor!\n"); return 1; }
l_yor = (int)xoryor;

      if (l_xor != HRAP_XOR){
         printf("EXITING!! In xmrg file: %s \n   xor parameter does not match defined xor (%d != %d)\n",infile, l_xor, HRAP_XOR);
	 if (nc_close(ncid) != NC_NOERR) printf("Error closing file %s !!\n", infile);
         return 1;
      }
      if (l_yor != HRAP_YOR){
         printf("EXITING!! In xmrg file: %s \n   yor parameter does not match defined yor (%d != %d)\n",infile, l_yor, HRAP_YOR);
	 if (nc_close(ncid) != NC_NOERR)  printf("Error closing file %s !!\n", infile);
         return 1;
      }
      if (l_hrap_x != HRAP_X){
         printf("EXITING!! In xmrg file: %s \n   hrap_x parameter does not match defined hrap_x (%d != %d)\n",infile, l_hrap_x, HRAP_X);
	 if (nc_close(ncid) != NC_NOERR) printf("Error closing file %s !!\n", infile);
         return 1;
      }
      if (l_hrap_y != HRAP_Y){
         printf("EXITING!! In xmrg file: %s \n   hrap_y parameter does not match defined hrap_y (%d != %d)\n",infile, l_hrap_y, HRAP_Y);
	 if (nc_close(ncid) != NC_NOERR) printf("Error closing file %s !!\n", infile);
         return 1;
      }

/* read in gridded data */
if (nc_inq_varid(ncid,"amountofprecip",&amountofprecip_id) != NC_NOERR)			{ printf("Error nc_inq_varid for amountofprecip!\n"); return 1; }

if (nc_inq_vartype(ncid,amountofprecip_id, &preciptype) != NC_NOERR){
	printf("Error nc_inq_varid for amountofprecip!\n");
   return 1;
}

if (preciptype == NC_SHORT){
	if (nc_get_vara_short(ncid,amountofprecip_id,start,count,*preciparray) != NC_NOERR){
   	printf("Error nc_get_vara_short for amountofprecip!\n");
      return 1;
   }
}
else { /* should be NC_INT */
	if (nc_get_vara_int(ncid,amountofprecip_id,start,count,*ipreciparray) != NC_NOERR){
   	printf("Error nc_get_vara_int for amountofprecip!\n");
      return 1;
   }
}

	
/* close netcdf */
if (nc_close(ncid) != NC_NOERR)					{ printf("ERROR -- could not close file %s !!\n", infile); return 1; }

printf("finished reading %s\n",infile);


/*open output file for writing*/
sprintf(outfile, "%s/%s.txt", OUTPUT_DIR, inputdate);
if ((out_file = fopen(outfile, "wt+")) != NULL) {
	counter = 0;
	fprintf(out_file, "\"id\", \"hrapx\", \"hrapy\", \"lat\", \"long\", \"value\"\n");
	for (i = 0; i< HRAP_Y; i++) {
		for (j = 0; j< HRAP_X; j++) {
      	if (preciptype == NC_SHORT){
				if (preciparray[i][j] < 0 )
					value = preciparray[i][j];
				else
         		value = preciparray[i][j] / 2540.0;
         }
         else {
				if (ipreciparray[i][j] < 0 )
					value = ipreciparray[i][j];
				else
         		value = ipreciparray[i][j] / 2540.0;
         }
         
			hrap.x = j + HRAP_XOR + 0.5;
			hrap.y = i + HRAP_YOR + 0.5;
			latlon = HrapToLatLong(hrap);
			fprintf(out_file, "%d, %d, %d, %f, -%f, %f\n",counter, j+HRAP_XOR, i+HRAP_YOR, latlon.y, latlon.x, value);
	}	}
	fclose(out_file);
} else {
	printf("ERROR -- could NOT open output file %s !!\n", outfile);
	return 1;
   }
printf("finished writing %s\n",outfile);

return 0;
}
