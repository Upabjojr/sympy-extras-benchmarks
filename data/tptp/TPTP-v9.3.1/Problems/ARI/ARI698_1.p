%------------------------------------------------------------------------------
% File     : ARI698_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Solve simple system of linear equations, with parameter N
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : simplify21.pri [BHS07]
%          : poly_simplify21.p [Rue14]

% Status   : Theorem
% Rating   : 0.00 v9.3.0, 0.12 v7.5.0, 0.20 v7.4.0, 0.12 v7.3.0, 0.17 v7.0.0, 0.14 v6.4.0, 0.00 v6.3.0
% Syntax   : Number of formulae    :   19 (  11 unt;   7 typ;   0 def)
%            Number of atoms       :   17 (  17 equ)
%            Maximal formula atoms :    6 (   1 avg)
%            Number of connectives :    5 (   0   ~;   0   |;   5   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    6 (   1 avg)
%            Maximal term depth    :    7 (   2 avg)
%            Number arithmetic     :  139 (   0 atm;  93 fun;  46 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :   13 (   7 usr;  10 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
tff(x_type,type,
    n: $int ).

tff(x6_type,type,
    x6: $int ).

tff(x5_type,type,
    x5: $int ).

tff(x4_type,type,
    x4: $int ).

tff(x3_type,type,
    x3: $int ).

tff(x2_type,type,
    x2: $int ).

tff(x1_type,type,
    x1: $int ).

tff(eq1,axiom,
    n = 1000 ).

tff(eq2,axiom,
    $sum($sum($sum($sum($sum($product(1,x6),$product(n,x5)),$product(n,x4)),$product(n,x3)),$product(n,x2)),$product(n,x1)) = 0 ).

tff(eq3,axiom,
    $difference($difference($difference($difference($difference($product(n,x6),x5),x4),x3),x2),x1) = 0 ).

tff(eq4,axiom,
    $difference($difference($difference($difference($sum($product(n,x6),$product(1,x5)),x4),x3),x2),x1) = 0 ).

tff(eq5,axiom,
    $sum($sum($sum($sum($sum($product(n,x6),$product(0,x5)),$product(1,x4)),$product(1,x3)),$product(1,x2)),$product(1,x1)) = 0 ).

tff(eq6,axiom,
    $sum($sum($sum($difference($sum($product(n,x6),$product(0,x5)),x4),$product(1,x3)),$product(1,x2)),$product(1,x1)) = 0 ).

tff(eq7,axiom,
    $difference($difference($difference($sum($sum($product(n,x6),$product(0,x5)),$product(0,x4)),x3),x2),x1) = 0 ).

tff(eq8,axiom,
    $difference($difference($sum($sum($sum($product(n,x6),$product(0,x5)),$product(0,x4)),$product(1,x3)),x2),x1) = 0 ).

tff(eq9,axiom,
    $sum($sum($sum($sum($sum($product(n,x6),$product(0,x5)),$product(0,x4)),$product(0,x3)),$product(1,x2)),$product(1,x1)) = 0 ).

tff(eq10,axiom,
    $sum($difference($sum($sum($sum($product(n,x6),$product(0,x5)),$product(0,x4)),$product(0,x3)),x2),$product(1,x1)) = 0 ).

tff(eq11,axiom,
    $difference($sum($sum($sum($sum($product(n,x6),$product(0,x5)),$product(0,x4)),$product(0,x3)),$product(0,x2)),x1) = 0 ).

tff(conj,conjecture,
    ( ( x6 = 0 )
    & ( x5 = 0 )
    & ( x4 = 0 )
    & ( x3 = 0 )
    & ( x2 = 0 )
    & ( x1 = 0 ) ) ).

%------------------------------------------------------------------------------
