settings.outformat="pdf";
settings.render=8;
defaultpen(fontsize(10pt));
size(6cm, 0);

//Cuadrado
real a,b, flecha;
a = 12.5;
flecha = 5;
fill(box((0,0), (a,a)), rgb(161/255,209/255,238/255));
draw((-flecha,a/2) -- (0,a/2), arrow=Arrow);
label("$q_x$", (-flecha,a/2), align=W);
draw((a,a/2) -- (a+flecha,a/2), arrow=Arrow);
label("$q_x + \frac{dq_x}{dx}$", (a+flecha,a/2), align=E);
draw((a/2,-flecha) -- (a/2,0), arrow=Arrow);
label("$Q_g$", (a/2,-flecha), align=S);