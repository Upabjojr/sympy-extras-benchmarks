%------------------------------------------------------------------------------
% File     : ARI645_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Prove that d >= 0, b >= a, a > 0 imply d / b <= d / a
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : inequations0.pri [BHS07]
%          : division3.p [Rue14]

% Status   : Theorem
% Rating   : 0.50 v9.1.0, 0.60 v9.0.0, 0.50 v8.2.0, 0.67 v7.5.0, 0.80 v7.4.0, 0.83 v7.3.0, 0.75 v7.1.0, 0.83 v7.0.0, 1.00 v6.3.0
% Syntax   : Number of formulae    :    4 (   0 unt;   3 typ;   0 def)
%            Number of atoms       :    4 (   0 equ)
%            Maximal formula atoms :    4 (   4 avg)
%            Number of connectives :    3 (   0   ~;   0   |;   2   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    4 (   4 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :    8 (   4 atm;   2 fun;   2 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    3 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    5 (   3 usr;   4 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
tff(a_type,type,
    a: $int ).

tff(a_type_001,type,
    b: $int ).

tff(a_type_002,type,
    d: $int ).

tff(conj,conjecture,
    ( ( $greatereq(d,0)
      & $greatereq(b,a)
      & $greater(a,0) )
   => $lesseq($quotient_e(d,b),$quotient_e(d,a)) ) ).

%------------------------------------------------------------------------------
