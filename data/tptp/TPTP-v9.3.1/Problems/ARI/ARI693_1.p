%------------------------------------------------------------------------------
% File     : ARI693_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Solve simple system of linear equations
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : simplify18.pri [BHS07]
%          : poly_simplify18.p [Rue14]

% Status   : Theorem
% Rating   : 0.80 v9.3.0, 0.88 v8.1.0, 0.50 v7.5.0, 0.70 v7.4.0, 0.75 v7.3.0, 0.67 v7.0.0, 0.86 v6.4.0, 1.00 v6.3.0
% Syntax   : Number of formulae    :    8 (   4 unt;   4 typ;   0 def)
%            Number of atoms       :    4 (   4 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :    4 (   2 avg)
%            Number arithmetic     :   31 (   0 atm;  15 fun;  16 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :   19 (   4 usr;  16 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
tff(x_type,type,
    x: $int ).

tff(a_type,type,
    a: $int ).

tff(z_type,type,
    z: $int ).

tff(y_type,type,
    y: $int ).

tff(eq1,axiom,
    $sum($product(3,x),$product(5,a)) = 1 ).

tff(eq2,axiom,
    $sum($product(7,z),$product(-1,$product(17,x))) = 4 ).

tff(eq3,axiom,
    $sum($sum($product(2,y),$product(7,x)),$product(-1,$product(-1,34))) = 0 ).

tff(conj,conjecture,
    $remainder_t($sum(z,116),170) = 0 ).

%------------------------------------------------------------------------------
