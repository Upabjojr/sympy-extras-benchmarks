%------------------------------------------------------------------------------
% File     : ARI657_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Satisfy a <= -3, a*b <= 5
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : nonLinInEqExample1.pri [BHS07]
%          : nonLinInEqExample1.p [Rue14]

% Status   : Satisfiable
% Rating   : 0.00 v6.4.0, 1.00 v6.3.0
% Syntax   : Number of formulae    :    4 (   2 unt;   2 typ;   0 def)
%            Number of atoms       :    2 (   0 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :    5 (   2 atm;   1 fun;   2 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    5 (   2 usr;   4 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_SAT_NEQ_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
tff(a_type,type,
    a: $int ).

tff(b_type,type,
    b: $int ).

tff(conj,axiom,
    $lesseq(a,-3) ).

tff(conj_001,axiom,
    $greatereq(5,$product(a,b)) ).

%------------------------------------------------------------------------------
