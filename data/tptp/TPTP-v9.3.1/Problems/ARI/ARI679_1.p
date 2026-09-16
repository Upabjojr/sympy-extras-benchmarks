%------------------------------------------------------------------------------
% File     : ARI679_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Prove equivalence of nonlinear inequalities
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : quadraticInEq4.pri [BHS07]
%          : quadraticInEq4.p [Rue14]

% Status   : Theorem
% Rating   : 0.25 v9.1.0, 0.40 v9.0.0, 0.25 v8.2.0, 0.33 v7.5.0, 0.20 v7.4.0, 0.50 v7.3.0, 0.62 v7.1.0, 0.67 v7.0.0, 0.83 v6.4.0, 1.00 v6.3.0
% Syntax   : Number of formulae    :    5 (   2 unt;   2 typ;   0 def)
%            Number of atoms       :    4 (   0 equ)
%            Maximal formula atoms :    2 (   1 avg)
%            Number of connectives :    1 (   0   ~;   0   |;   0   &)
%                                         (   1 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    2 (   1 avg)
%            Maximal term depth    :    3 (   1 avg)
%            Number arithmetic     :   17 (   4 atm;   6 fun;   7 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    6 (   2 usr;   4 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
tff(d_type,type,
    d: $int ).

tff(c_type,type,
    c: $int ).

tff(conj,axiom,
    $lesseq(3,d) ).

tff(conj_001,axiom,
    $lesseq(2,c) ).

tff(conj_002,conjecture,
    ( $lesseq($product(2,3),$product(c,d))
  <=> $lesseq($product(2,$difference(d,3)),$product(c,$difference(d,3))) ) ).

%------------------------------------------------------------------------------
