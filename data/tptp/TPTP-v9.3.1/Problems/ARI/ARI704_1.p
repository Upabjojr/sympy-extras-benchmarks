%------------------------------------------------------------------------------
% File     : ARI704_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Solve simple system of linear equations
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : simplify27.pri [BHS07]
%          : poly_simplify27.p [Rue14]

% Status   : Satisfiable
% Rating   : 0.00 v6.3.0
% Syntax   : Number of formulae    :    9 (   4 unt;   5 typ;   0 def)
%            Number of atoms       :    4 (   4 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :    3 (   1 avg)
%            Number arithmetic     :   19 (   0 atm;   9 fun;  10 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :   14 (   5 usr;  12 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_SAT_EQU_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
tff(x6_type,type,
    x6: $int ).

tff(x5_type,type,
    x5: $int ).

tff(x3_type,type,
    x3: $int ).

tff(x4_type,type,
    x4: $int ).

tff(x2_type,type,
    x2: $int ).

tff(eq1,axiom,
    x6 = 0 ).

tff(eq2,axiom,
    $sum($product(2,x5),$product(1,x3)) = 0 ).

tff(eq3,axiom,
    $sum($product(5,x4),$product(3,x2)) = 0 ).

tff(eq4,axiom,
    $sum($product(7,x3),$product(11,x2)) = 0 ).

%------------------------------------------------------------------------------
