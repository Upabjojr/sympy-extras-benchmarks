%------------------------------------------------------------------------------
% File     : ARI668_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : 11*a + 7*b = 1 and c >= a imply a*c <= 0 | a*c >= 4
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : quadraticInEq14.pri [BHS07]
%          : quadraticInEq14.p [Rue14]

% Status   : Theorem
% Rating   : 0.40 v9.3.0, 0.38 v9.1.0, 0.50 v9.0.0, 0.38 v8.2.0, 0.50 v7.0.0, 0.71 v6.4.0, 1.00 v6.3.0
% Syntax   : Number of formulae    :    6 (   2 unt;   3 typ;   0 def)
%            Number of atoms       :    4 (   1 equ)
%            Maximal formula atoms :    2 (   1 avg)
%            Number of connectives :    1 (   0   ~;   1   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    2 (   1 avg)
%            Maximal term depth    :    3 (   1 avg)
%            Number arithmetic     :   13 (   3 atm;   5 fun;   5 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    3 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :   10 (   3 usr;   8 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
tff(a_type,type,
    a: $int ).

tff(b_type,type,
    b: $int ).

tff(c_type,type,
    c: $int ).

tff(conj,axiom,
    $sum($product(11,a),$product(7,b)) = 1 ).

tff(conj_001,axiom,
    $lesseq(a,c) ).

tff(conj_002,conjecture,
    ( $lesseq(4,$product(a,c))
    | $greatereq(0,$product(a,c)) ) ).

%------------------------------------------------------------------------------
