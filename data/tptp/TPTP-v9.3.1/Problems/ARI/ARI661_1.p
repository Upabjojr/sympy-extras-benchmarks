%------------------------------------------------------------------------------
% File     : ARI661_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Prove that a*a*a*a*a >= 40 and a >= 3 are equivalent
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : nonLinInEqExample2.pri [BHS07]
%          : nonLinInEqExample2d.p [Rue14]

% Status   : Theorem
% Rating   : 0.25 v9.1.0, 0.40 v9.0.0, 0.25 v8.2.0, 0.17 v7.5.0, 0.20 v7.4.0, 0.17 v7.3.0, 0.12 v7.1.0, 0.17 v7.0.0, 0.50 v6.4.0, 1.00 v6.3.0
% Syntax   : Number of formulae    :    2 (   0 unt;   1 typ;   0 def)
%            Number of atoms       :    2 (   0 equ)
%            Maximal formula atoms :    2 (   2 avg)
%            Number of connectives :    1 (   0   ~;   0   |;   0   &)
%                                         (   1 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    2 (   2 avg)
%            Maximal term depth    :    5 (   2 avg)
%            Number arithmetic     :    8 (   2 atm;   4 fun;   2 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    4 (   1 usr;   3 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
tff(a_type,type,
    a: $int ).

tff(conj,conjecture,
    ( $lesseq(40,$product($product($product($product(a,a),a),a),a))
  <=> $lesseq(3,a) ) ).

%------------------------------------------------------------------------------
