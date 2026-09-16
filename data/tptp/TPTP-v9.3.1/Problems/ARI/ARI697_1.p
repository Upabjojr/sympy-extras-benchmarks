%------------------------------------------------------------------------------
% File     : ARI697_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Solve simple system of linear equations
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : simplify20.pri [BHS07]
%          : poly_simplify20.p [Rue14]

% Status   : Theorem
% Rating   : 0.60 v9.3.0, 0.62 v9.1.0, 0.75 v8.1.0, 0.50 v7.0.0, 0.71 v6.4.0, 0.33 v6.3.0
% Syntax   : Number of formulae    :    9 (   4 unt;   5 typ;   0 def)
%            Number of atoms       :    4 (   4 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :    7 (   2 avg)
%            Number arithmetic     :   54 (   0 atm;  31 fun;  23 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :   22 (   5 usr;  18 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
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

tff(eq1,axiom,
    $sum($difference($sum($difference($product(-1,$product(2,x2)),$product(5,x1)),x3),x4),x5) = 0 ).

tff(eq2,axiom,
    $sum($sum($sum($sum($product(9,x1),$product(62,x2)),$product(-1,$product(5,x3))),$product(-1,$product(3,x4))),$product(101,x5)) = 0 ).

tff(eq3,axiom,
    $sum($sum($sum($sum($product(56,x1),$product(-1,$product(34,x2))),$product(-1,$product(11,x3))),$product(67,x4)),$product(-1,$product(98,x5))) = 0 ).

tff(conj,conjecture,
    $remainder_t(x5,2) = 0 ).

%------------------------------------------------------------------------------
