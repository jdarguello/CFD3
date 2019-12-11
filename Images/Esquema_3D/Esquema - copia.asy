settings.outformat="png";
settings.render=16;

import three;
size(4cm, 0);

//Dimensiones - Sección transversal
real H = 3;
real Ancho = 3;
real h = 0.5;
real ancho = 1;

real L = 5;

//Ejes coordenados
draw((Ancho,0,0) -- (5,0,0), blue);
draw((0,L,0) -- (0,6,0), green);
draw((0,0,H) -- (0,0,H+1), red);

//Función - Líneas ocultas
void Hidden (real x, real y, real z, real dim, real line_size = 0.125, real spaceLine = 0.125, int r=0, int g=0, int b=0, string direction = 'z'){
    real dimension;
    if (direction == 'z') {
        dimension = dim - z;
    } else if (direction == 'x') {
        dimension = dim - x;
    } else {
        dimension = dim - y;
    }
    int signo = 1;
    if (dimension < 0) {
        dimension = -1*dimension;
        signo = -1;
    }
    int num_lineas = round(dimension/(line_size+spaceLine));
    real suma_ant = 0;
    real suma;
    for (int i=0; i< num_lineas; i=i+1) {
        suma = suma_ant + signo*line_size;
        if (direction == 'z') {
           draw((x,y,z+suma_ant) -- (x,y,z+suma), rgb(r/255,g/255,b/255)); 
        } else if (direction == 'x') {
            draw((x+suma_ant,y,z) -- (x+suma,y,z), rgb(r/255,g/255,b/255)); 
        } else {draw((x,y+suma_ant,z) -- (x,y+suma,z), rgb(r/255,g/255,b/255)); }
        suma_ant = suma + signo*spaceLine;
    }
}

//Sección transversal - Función
void Trans(real x, real y, real z) {
    Hidden(x,y,z, h);
    Hidden(x,y,z+h, (Ancho-ancho)/2, direction = 'x');
    Hidden(x+(Ancho-ancho)/2,y,z+h, H - h);
    Hidden(x+(Ancho-ancho)/2,y,z+H-h, 0, direction='x');
    Hidden(x,y,z+H-h, H);
    Hidden(x,y,z+H, Ancho, direction='x');
    //draw((x,y,z+H) -- (Ancho,y,z+H));
    draw((x+Ancho,y,z+H) -- (Ancho,y,z+H-h));
    Hidden(x+Ancho,y,H-h, (Ancho+ancho)/2, direction = 'x');
    draw((x+(Ancho+ancho)/2,y,z+H-h) -- ((Ancho+ancho)/2,y,z+h));
    draw((x+(Ancho+ancho)/2,y,z+h) -- (Ancho, y,z+h));
    draw((x+Ancho, y,z+h) -- (Ancho,y,0z));
    Hidden(x+Ancho,y,0z,0, direction='x');
}

//Secciones
Trans(0,0,0);
Trans(0,L,0);

//Lateral oculto
Hidden(0,0,0, L, direction='y');
Hidden(0,0,h, L, direction='y');
Hidden((Ancho-ancho)/2,0,h, L, direction='y');
Hidden((Ancho-ancho)/2,0,H-h, L, direction='y');
Hidden(0,0,H-h, L, direction='y');
Hidden(0,0,H, L, direction='y');

//Lateral visible
draw((Ancho,0,H) -- (Ancho,L,H));
draw((Ancho,0,H-h) -- (Ancho,L,H-h));
draw(((Ancho+ancho)/2,0,H-h) -- ((Ancho+ancho)/2,L,H-h));
draw(((Ancho+ancho)/2,0,h) -- ((Ancho+ancho)/2,L,h));
draw((Ancho,0,h) -- (Ancho,L,h));
draw((Ancho,0,0) -- (Ancho,L,0));

//Correcciones Generales
draw((Ancho,0,H-h) -- ((Ancho+ancho)/2,0,H-h));
draw((Ancho,L,H-h) -- ((Ancho+ancho)/2,L,H-h));
draw((Ancho,L,0) -- (0,L,0));
draw((0,L,0) -- (0,L,h));
draw((0,L,h) -- ((Ancho-ancho)/2,L,h));
draw(((Ancho-ancho)/2,L,h) -- (((Ancho-ancho)/2,L,H-h)));
draw(((Ancho-ancho)/2,L,H-h) -- (0,L,H-h));
draw((0,L,H-h) -- (0,L,H));
draw((0,L,H) -- (Ancho,L,H));

//Elemento
real Ex, Ey, Ez, refx, refy, refz;
Ex = 0.4;
Ey = Ex;
Ez = Ex;

refx = (Ancho - Ex)/2;
refy = (L-Ey)/2;
refz = (H-Ez)/2;

//Elemento - líneas ocultas
draw(box((refx, refy, refz), (refx+Ex, refy+Ey, refz+Ez)), rgb(108/255, 214/255, 246/255));
/*
real line, space;
line = 0.125/2;
space = line;
Hidden(refx, refy, refz, refz + Ez, line_size = line, spaceLine = space, r=108, g = 214, b = 246);
Hidden(refx, refy, refz, refx + Ex, line_size = line, spaceLine = space, r=108, g = 214, b = 246, direction='x');
Hidden(refx, refy, refz, refy + Ey, line_size = line, spaceLine = space, r=108, g = 214, b = 246, direction='y');
draw((refx+Ex, refy, refz) -- (refx+Ex, refy + Ey, refz), rgb(108/255,214/255,246/255));
draw((refx+Ex, refy, refz) -- (refx+Ex, refy, refz + Ez), rgb(108/255,214/255,246/255));
draw((refx, refy+Ey, refz) -- (refx,refy, refz+Ez), rgb(108/255,214/255,246/255));
*/