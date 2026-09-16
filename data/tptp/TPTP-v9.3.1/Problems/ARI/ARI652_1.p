%------------------------------------------------------------------------------
% File     : ARI652_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Prove that a + 4 > 2, -2 <= -3 - a imply a*a = 1
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : inequations1.pri [BHS07]
%          : inequations1.p [Rue14]

% Status   : Theorem
% Rating   : 0.00 v9.3.0, 0.12 v8.2.0, 0.25 v7.5.0, 0.30 v7.4.0, 0.25 v7.3.0, 0.17 v7.0.0, 0.43 v6.4.0, 0.50 v6.3.0
% Syntax   : Number of formulae    :    4 (   3 unt;   1 typ;   0 def)
%            Number of atoms       :    3 (   1 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :   10 (   2 atm;   3 fun;   5 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    3 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    9 (   1 usr;   6 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
tff(a_type,type,
    a: $int ).

tff(conj,axiom,
    $less(2,$sum(a,4)) ).

tff(conj_001,axiom,
    $lesseq(-2,$difference(-3,a)) ).

tff(conj_002,conjecture,
    $product(a,a) = 1 ).

%------------------------------------------------------------------------------
