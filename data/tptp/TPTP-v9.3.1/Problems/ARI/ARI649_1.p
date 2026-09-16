%------------------------------------------------------------------------------
% File     : ARI649_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : a*a = 25, b*b*b = -125, a < 0 imply a = b
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : simplify5.pri [BHS07]
%          : ineqs_simplify5a.p [Rue14]

% Status   : Theorem
% Rating   : 0.20 v9.3.0, 0.25 v9.1.0, 0.38 v9.0.0, 0.25 v8.2.0, 0.38 v7.5.0, 0.40 v7.4.0, 0.38 v7.3.0, 0.33 v7.0.0, 0.57 v6.4.0, 1.00 v6.3.0
% Syntax   : Number of formulae    :    6 (   4 unt;   2 typ;   0 def)
%            Number of atoms       :    4 (   3 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :    3 (   1 avg)
%            Number arithmetic     :    7 (   1 atm;   3 fun;   3 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    6 (   2 usr;   5 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
tff(a_type,type,
    a: $int ).

tff(b_type,type,
    b: $int ).

tff(conj,axiom,
    $less(a,0) ).

tff(conj_001,axiom,
    $product(a,a) = 25 ).

tff(conj_002,axiom,
    $product($product(b,b),b) = -125 ).

tff(conj_003,conjecture,
    a = b ).

%------------------------------------------------------------------------------
