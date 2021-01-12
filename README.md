# Elliptic Curve Cryptography

* [Background](##Background)
  * [What are Elliptic Curves](###What%20are%20Elliptic%20Curves?)
  * [Addition and Subtraction](###What does it mean to add or subtract points on an elliptic curve?)
  * [Multiplication and Division](###Multiplication and Division)
  * [Co-ordinate Structure](### Affine vs Projective co-ordinates)
  * [Finite Fields](###Finite Fields)
  * [Why we keep different curve types](### Why aren't all curves just converted all forms back into Short Weierstrass form)
* [Performable Operations](##Operations performable)
  * [Basic Operations](###Basic Operations)
  * [Finding y from x](###Computing Y for a given points)
  * [Loading Points or Curves](###Loading Points or curves)
* [Diffie Hellman](##Diffie Hellman)
* [Elgamel](##Elgamel)
* [ECDSA](##Elliptic Curve Digital Signature Algorithm)


## Background

### What are Elliptic Curves?
Elliptic curves is any curve which can be expressed in the form y<sup>2</sup> = x<sup>3</sup> + ax + b; where a,b are arbitrary constants.
For the majority of this document I will be talking about 3 forms of elliptic curve :

  * **Short Weierstrass** : y<sup>2</sup> = x<sup>3</sup> + ax + b
  * **Mongomery**         : ay<sup>2</sup> = x<sup>3</sup> + bx<sup>2</sup> + x
  * **EdwardsCurve**      : x<sup>2</sup> + y<sup>2</sup> = a<sup>2</sup>(1+ bx<sup>2</sup>y<sup>2</sup>)

This is they are the 3 curve types supported by my program as they are the most useful for cryptography, and while (due to the definition of elliptic curves) all can be expressed as Short Weierstrass form it is often more useful to leave them in their other forms, as equations for addition, subtraction and doubling differ between them.

### What does it mean to add or subtract points on an elliptic curve?
The short Weierstrass is the curve on which addition is the easiest to explain so that is one I will explain it over, however there are differing equations for all types.

For a short Weierstrass curve to add 2 points you take the line going through both points and then the point where is intersects the graph again is the negative of their sum. So to find A + B first find the equation of the line going through them, work out its other intersection with the curve and then flip that in the x axis. However there are some holes in this explanation of adding, like what happens when the 2 points being added are the same or when the curve doesn't intersect with the curve again. When a point is being added to itself simply take the tangent at that point and use that as the equivalent of the line going through the 2 points. There are some times when the line won't intersect with the curve again, but due to the shape of the Short Weierstrass curve this only happens when the points are vertically above each other and when this happens we simply say that they intersect again at a point at infinity and leave it at that (Due to the fact that A + (-A) = PAI, the PAI is also the additive identity).

From the geometric definition of addition and subtraction comes the algebraic equations for all the Short Weierstrass curve and therefore all 3 other curves due to their ability to represented as Short Weierstrass Curves. For (x<sub>1</sub>, y<sub>1</sub>) + (x<sub>2</sub>, y<sub>2</sub>) = (x<sub>3</sub>, y<sub>3</sub>) formulas for x<sub>3</sub> and  y<sub>3</sub> are show below :

* **Short Weierstrass** :
  * gradient = g = (y<sub>2</sub> - y<sub>1</sub>) * (x<sub>2</sub> - x<sub>1</sub>)<sup>-1</sup>
  * x<sub>3</sub> = g<sup>2</sup> - x<sub>2</sub> - x<sub>1</sub>
  * y<sub>3</sub> =  y<sub>2</sub> + g(x<sub>2</sub> - x<sub>1</sub>) // still requires maths
* **Mongomery**         :
  * gradient = g = (y<sub>2</sub> - y<sub>1</sub>) * (x<sub>2</sub> - x<sub>1</sub>)<sup>-1</sup>
  * x<sub>3</sub> = a*g<sup>2</sup> - b - x<sub>2</sub> - x<sub>1</sub>
  * y<sub>3</sub> = g(x<sub>3</sub> - x<sub>1</sub>) + y<sub>1</sub>
* **EdwardsCurve**      :
  * x<sub>3</sub> = (y<sub>1</sub>y<sub>2</sub> - x<sub>1</sub>x<sub>2</sub>) * (a*(1 - dx<sub>1</sub>x<sub>2</sub>y<sub>1</sub>y<sub>2</sub>))
  * y<sub>3</sub> = (x<sub>1</sub>y<sub>2</sub> + x<sub>2</sub>y<sub>1</sub>) * (a*(1 + dx<sub>1</sub>x<sub>2</sub>y<sub>1</sub>y<sub>2</sub>))

### Multiplication and Division

Multiplication by a scalar can be simply done by the doubling and adding method and this is fairly computationally easy; just continually double the point and if required add it to the result. However division by a scalar is far more difficult, and there are no particularly efficient methods to perform division (at least with the curves we shall be using for cryptography). This fact that it is easy to multiply by a scalar and very difficult to divide forms the basis of elliptic curve cryptography, and this discrete logarithm problem is far difficult than other discrete logarithm problems used in cryptography, for instance a 512 bit ECC key provides the same security as a 2048 RSA key.

### Affine vs Projective co-ordinates

Affine co-ordinates (often called Cartesian co-ordinates) are the ones that most people are used to (x,y), while projective co-ordinates are (X,Y,Z) where x = X/Z and y = Y/Z. Affine co-ordinates make the most intuitive sense as they are the ones we are used to using however they can be more computational difficult when performing elliptic curve operations than projective co-ordinates. This is because with projective co-ordinates there is no need for a division or inverse, which is far more computationally difficult than multiplication, which outweighs the increased storage space required for storing 3 values instead of 2.

### Finite Fields

In the real world we have a problem if we take a elliptic curve and allow its x and y co-ordinates to be any real number, we get values which can't be precisely stored on a computer and so quickly floating point errors compound. So instead of using the field of all real number we define the field as mod a number n (F<sub>n</sub>), and typically n is a large prime number. This gets rid of the problem of the problem of storing fractions as numbers can only be integers in the range of 0 to n, however it does mean that we do have to calculate modular inverses (which is why we use prime numbers as our mod so that they always exist) which can be computationally difficult; which is why we typically use projective co-ordinates, so we only need to 2 inverses at the end to work out x and y from (X,Y,Z).

### Why aren't all curves just converted all forms back into Short Weierstrass form

There are 2 main reasons that we might keep curves in their original forms instead of keeping them all in Short Weierstrass from    :

* It may create nicer constant terms to have them in their original form
* Often operations are faster to perform on other curves as opposed to the Short Weierstrass form
    * Or in the case of Edwards curves it is more complete; not needing the additionial inclusion of the point at infinity in addition to being a faster process

## Operations performable

### Basic Operations
For all curve types :

* **Addition**                  :
    * Can add any 2 points so long as they are on the same curve.
    * Affine co-ordinates - Point1.add(Point2); Point1 will be overwritten with result
    * Projective co-ordinates - Point1.baseadd(Point2); Point1 will be overwritten with result
* **Double**                    :
    * Can double any point
    * Affine co-ordinates - Point1.double(); Point1 will be overwritten with result
    * Projective co-ordinates - Point1.basedouble(); Point1 will be overwritten with result
* **Subtraction**               :
    * Can subtract any 2 points so long as they are on the same curve
    * Affine co-ordinates - Point1.sub(Point2); Point1 will be overwritten with result
    * Projective co-ordinates - Point.basesub(Point2); Point1 will be overwritten with result
* **Multplication by scalar**   :
    * Can multiply any point by a any scalar positive or negative or zero
    * Affine co-ordinates - Point1.mult(number); Point1 will be overwritten with result
    * Projective co-ordinates - Point1.basemult(number); Point1 will be overwritten with result
* **Modular inverse**           :
    * Can calculate modular inverse for any number as long as mod > 0
    * modular_inverse = inv(number,mod); will return result between 0 and mod
* **Negate**                    :
    * Can negate any point; in projective or affine co-ordinates
    * Point1.negate(); Point1 will be overwritten with result
* **Convert to affine**         :
    * Can take any point and convert from projective to affine co-ordinates
    * Point1.toaffine(); Point1 will be overwritten with affine instead of projective co-ordinates
* **Copy**                      :
    * Can copy any point or curve
    * Returns an object with the same parameters as the original

### Computing Y for a given points

For any point with a x co-ordinate which is on the curve the y co-ordinate can be calculated. As it is a operation performed by the point object first it must be defined with a random y co-ordinate (we suggest something like null so that if it accidentally used before the actual y is calculated it will simply throw an error).
* It also converts any point into affine co-ordinates before it begins to calculate the y as that simplifies calculation
* You call it as such - Point1.find_y()
  * This overwrites Point1 with result

### Loading Points or curves

Allows you to load in points or curves as you need them with these functions  :

* Point1 = load_point(point_name)
  * Will load the point with name = point_name and curve for the point into objects from the text database
  * The point will be loaded into Point1 and the curve into Point1.curve
* Curve1 = load_curve(curve_name)
  * Will load the curve with name = curve_name from text database into an object

The names of all curves currently supported are stored in list_of_curves, so if you are unsure as to which curves are supported you can check there. If you want to see all supported curves with their parameters call show_base_parameters() which outputs those.

## Diffie Hellman

Functions referenced here can be found in diffie_hellman.py

To perform Diffie Hellman key exchange first agree with the other party a particular base point. Then call **start_step(point)**, this will generate a cryptographically secure secret and then return point*secret. This needs to be shared with the other party and they need to share the result of their start_step with you, then when the other point is received call **end_step(other_point)** to calculate the shared secret and this will also delete the variable after it is no longer needed.

## Elgamel

Functions referenced here can be found in Elgamel.py

First the one receiving the message must publish their base point and public key but not the private key in some way so that the other party can safely access it and tell that those are the correct parameters. These parameters both private and public key can be generated from the base point using **gen_private_public_key(base_point)**.

If you are the one sending the message you need to call **encrypt(base_point, public_key, message)**, where message is an integer less than base_point//100. Be warned that this process of mapping this message to a point so there is a possibility that it won't be able to map to a point (although this change is miniscule). If this does happen it will throw an error.

If you have received a message then call **decrypt(private_key ,base_point, message_point)** and it will return the message that was encoded into the message_point


## Elliptic Curve Digital Signature Algorithm

First the one creating the signature needs to have published the base point they are using along with the public key but not the private key in some way that the other party can safely access it and tell that those are the correct parameters. These parameter both private and public key can be generated from the base point using **gen_private_public_key(base_point)**.

If you are the one creating the signature call **create_signature(base_point, private_key, message)** where message is a binary string. This will then return the signature pair r and s for the message.

If you need to check the signature call **verify(base_point, public_key, message, signature_pair)** where message is the binary message received. This will return True if it is the signature or false if it is not.
