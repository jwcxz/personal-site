[Dwitter](https://dwitter.net) is a site where users write JavaScript to create
demos in 140 characters or fewer.  The site provides a 1920×1080 canvas and a
few helper functions (e.g. `S(...)` returns `Math.sin(...)`).

I [have created a few "dweets"](https://www.dwitter.net/u/jwc), but I'm still
very much learning and experimenting with interesting techniques.

For example, here is a screen recording of a
[simple demo I created](https://www.dwitter.net/d/21060)
that computes a Lorenz attractor and spins the rendered graph around:

![Rotating Lorenz Attractor](/notes/201229-dwitter-js-demo-dev-notes/d-21060-rotating-lorenz-attractor.gif)

The code for it is as follows:

```js
// 140 characters (minus newline and indents added for readability)
for(c.width|=i=q=r=s=.1;i<t;b=4*i/t,
            x.fillRect(960+16*(q*C(t)+s*S(t)),540+20*r,b,b),i+=.01)
    o=r,r+=(q*(28-s)-r)/50,s+=(q*o-2*s)/50,q+=(o-q)/5
```

Some notes on compression techniques I've seen or employed follow.  I will
update these notes as I learn additional ones.


<!--break-->


[[toc]]


## Use of comma operator

The comma operator effectively concatenates multiple expressions and returns
the evaluated value of the final expression, so it makes sense to use it
extensively (see
[MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Comma_Operator)
for details).

This is useful in a variety of situations where a single expression is
expected.


## Optimal `for` statements

A few things can be done here:

1.  Obviate the need for `{}` encapsulation by joining statements with commas,
    e.g. `for(...)S1,S2,S3`.

2.  Use the `condition` expression to also update the iterator, e.g.
    `for(i=100;i--;)`

3.  Make use of the `final` expression space, e.g. `for(...;S3)S1,S2` saves one
    character compared to `for(...;)S1,S2,S3`.

Putting these together into an example:

```js
// before
for(i=0;i<100;i++) {
    S1;
    S2;
    S3;
}

// before, but no spaces or newlines
for(i=0;i<100;i++){S1;S2;S3;}

// after (saves 7 characters)
for(i=100;i--;S3)S1,S2
```


## Embedded `c.width` assignment

A simple way to clear the canvas prior to drawing a new frame is to set
`c.width`.  The easiest thing to do is to set `c.width=1920` at the beginning
of the code, but you can save two characters if you do something like
`c.width|=` in front of another assignment.  For example, if you have
`for(i=0;i<...`, you could do `for(c.width|=i=0;i<...`.  The assignment doesn't
necessarily have to be to `0` --- `c.width|=i=20` just extends the width of the
canvas a bit, for example, so it's not a big deal.


## Scope inclusion --- `with(x)`

Every invocation of a method of the `CanvasRenderingContext2D` instance `x`
incurs two additional characters (e.g. `x.fillRect()`).  If the subsequent code
can be a single statement, prepend the statement with `with(x)` if at least 4
methods/properties of `x` will be accessed (4 usages will save 1 character, 5
will save 3, etc.).  Those methods/properties will now be directly accessible
(e.g. `fillRect()` instead of `x.fillRect()`.


## Embedding other expressions within function invocations

Functions with no arguments or optional arguments can be paired with
expressions that return nothing (or whose return value do not affect the outer
function's invocation).  One example I've seen (and subsequently
[used](https://www.dwitter.net/d/21045)) is to embedded expressions within
`beginPath()` and `fill()`.

For example:

```js
// before
fillStyle=...,beginPath(),ellipse(...),fill()

//after (saves 2 characters)
beginPath(fillStyle=...),fill(ellipse(...))
```


## Inline variable assignment

Variables can be assigned within other statements.  This technique is sometimes
useful when an expression is used in multiple statements, particularly for
function arguments.

For example:

```js
// before
a=4*S(t),x.fillRect(...,...,a,a)

// after (saves 2 characters)
x.fillRect(...,...,a=4*S(t),a)
```

However, in most other cases, this technique has net zero effect, for example:

```js
// before
c=100-t,a=100+S(t)*c,d=C(t)*c

// after (no savings)
a=100+S(t)*(c=100-t),d=C(t)*c
```


## Other Resources

* [This analysis](https://medium.com/@r.l.bongers/visual-effect-analysis-animated-raindrops-682b83b87e09)
  of one of my [favorite dweets](https://www.dwitter.net/d/1494) breaks down a
  number of its techniques

    * E.g. `~~` is a clever way to achieve `(a>=0)?Math.floor(a):Math.ceil(a)`
