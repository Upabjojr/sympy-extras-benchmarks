%------------------------------------------------------------------------------
% File     : ARI694_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Solve simple system of linear equations
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : simplify19.pri [BHS07]
%          : poly_simplify19.p [Rue14]

% Status   : Theorem
% Rating   : 0.80 v9.3.0, 0.88 v8.1.0, 0.62 v7.5.0, 0.70 v7.4.0, 0.88 v7.3.0, 0.83 v7.0.0, 0.86 v6.4.0, 1.00 v6.3.0
% Syntax   : Number of formulae    :   20 (  10 unt;  10 typ;   0 def)
%            Number of atoms       :   10 (  10 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :    3 (   2 avg)
%            Number arithmetic     :   57 (   0 atm;  28 fun;  29 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :   18 (  10 usr;  15 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
tff(x0_type,type,
    x0: $int ).

tff(x1_type,type,
    x1: $int ).

tff(x2_type,type,
    x2: $int ).

tff(x3_type,type,
    x3: $int ).

tff(x4_type,type,
    x4: $int ).

tff(x5_type,type,
    x5: $int ).

tff(x6_type,type,
    x6: $int ).

tff(x7_type,type,
    x7: $int ).

tff(x8_type,type,
    x8: $int ).

tff(x9_type,type,
    x9: $int ).

tff(eq1,axiom,
    x0 = $sum($product(5,x1),1) ).

tff(eq2,axiom,
    $product(4,x1) = $sum($product(5,x2),1) ).

tff(eq3,axiom,
    $product(4,x2) = $sum($product(5,x3),1) ).

tff(eq4,axiom,
    $product(4,x3) = $sum($product(5,x4),1) ).

tff(eq5,axiom,
    $product(4,x4) = $sum($product(5,x5),1) ).

tff(eq6,axiom,
    $product(4,x5) = $sum($product(5,x6),1) ).

tff(eq7,axiom,
    $product(4,x6) = $sum($product(5,x7),1) ).

tff(eq8,axiom,
    $product(4,x7) = $sum($product(5,x8),1) ).

tff(eq9,axiom,
    $product(4,x8) = $sum($product(5,x9),1) ).

tff(conj,conjecture,
    $remainder_t($sum(x0,4),1953125) = 0 ).

%------------------------------------------------------------------------------
