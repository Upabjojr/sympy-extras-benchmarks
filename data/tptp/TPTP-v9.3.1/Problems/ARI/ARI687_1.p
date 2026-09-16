%------------------------------------------------------------------------------
% File     : ARI687_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Expand and rewrite polynomial
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : simplify11.pri [BHS07]
%          : poly_simplify11.p [Rue14]

% Status   : Theorem
% Rating   : 0.20 v9.3.0, 0.25 v9.1.0, 0.38 v9.0.0, 0.25 v8.2.0, 0.38 v7.5.0, 0.40 v7.4.0, 0.38 v7.3.0, 0.33 v7.0.0, 0.57 v6.4.0, 1.00 v6.3.0
% Syntax   : Number of formulae    :    6 (   4 unt;   2 typ;   0 def)
%            Number of atoms       :    4 (   4 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :   11 (   2 avg)
%            Number arithmetic     :   78 (   0 atm;  55 fun;  23 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :   12 (   2 usr;   9 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
tff(x_type,type,
    x: $int ).

tff(y_type,type,
    y: $int ).

tff(eq1,axiom,
    $sum($sum($sum($product($product($product(x,x),x),y),$product($product(x,x),y)),$product($product($product(3,x),x),x)),$product($product(2,x),x)) = 0 ).

tff(eq2,axiom,
    $sum($sum($sum($sum($difference($sum($product($product($product($product(2,x),x),x),y),$product(-1,$product(x,y))),y),$product($product($product(6,x),x),x)),$product(-1,$product($product(2,x),x))),$product(-1,$product(3,x))),3) = 0 ).

tff(eq3,axiom,
    $difference($sum($sum($sum($sum($product($product($product(3,x),x),y),$product($product(2,x),y)),y),$product($product(9,x),x)),$product(5,x)),3) = 0 ).

tff(conj,conjecture,
    $sum($product(2,$product($product(x,x),x)),$product(-1,$sum($product(5,x),$product(5,$product(x,x))))) = 0 ).

%------------------------------------------------------------------------------
