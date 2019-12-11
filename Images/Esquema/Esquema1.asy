settings.outformat="png";
unitsize(0.3cm);

//Tamaño del rectángulo
int a = 10*2;
int h = 6*2;

//Datos
Label H = Label("$H$", position=EndPoint, align=SW);
Label WW = Label("$W$", position=BeginPoint, align=NE);
Label Is = Label("$Isotermico - \theta = C$", position = MidPoint);
Label Ad1 = Label("$Adiabatico - \frac{\partial \theta}{\partial x} = 0$", position = MidPoint, align=W);
Label Ad2 = Label("$Adiabatico - \frac{\partial \theta}{\partial y} = 0$", position = MidPoint, align=N);
Label Bi = Label("$-\frac{\partial \theta}{\partial x} = Bi \theta$", position = MidPoint, align=E);
Label dif = Label("$\frac{\partial ^2 \theta}{\partial x^2} - \frac{\partial ^2 \theta}{\partial y ^2} = 0$", position = MidPoint, align=N, rgb(0,0,0));

//Ecuación diferencial
draw((0,h/2) -- (a,h/2), L = dif, rgb(1,1,1));

//Rectángulo
draw((0,0) -- (a,0), L = Is);
draw((0,h) -- (a,h), L = Ad2);
draw((0,0) -- (0,h), L = Ad1);
draw((a,0) -- (a,h), L = Bi);

//Generalidades
real t = 1;
draw((a-t, 0) -- (a-t,h), arrow=Arrows(), L=H);
draw((0,2*t) -- (a,2*t), arrow=Arrows(), L=WW);
