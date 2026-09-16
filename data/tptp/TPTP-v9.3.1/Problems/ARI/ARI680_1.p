%------------------------------------------------------------------------------
% File     : ARI680_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Solve system of nonlinear inequalities
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : quadraticInEq5.pri [BHS07]
%          : quadraticInEq5.p [Rue14]

% Status   : Theorem
% Rating   : 0.25 v9.1.0, 0.20 v9.0.0, 0.25 v8.2.0, 0.17 v7.5.0, 0.20 v7.4.0, 0.17 v7.3.0, 0.12 v7.1.0, 0.17 v7.0.0, 0.50 v6.4.0, 1.00 v6.3.0
% Syntax   : Number of formulae    :    7 (   4 unt;   3 typ;   0 def)
%            Number of atoms       :    4 (   0 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :    4 (   1 avg)
%            Number arithmetic     :   16 (   4 atm;   5 fun;   7 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :   11 (   3 usr;   9 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
tff(x_type,type,
    x: $int ).

tff(y_type,type,
    y: $int ).

tff(a_type,type,
    a: $int ).

tff(conj,axiom,
    $greater(4,$sum($product($product(3,x),y),$product(7,a))) ).

tff(conj_001,axiom,
    $less(3,$product(2,x)) ).

tff(conj_002,axiom,
    $less(1,y) ).

tff(conj_003,conjecture,
    $greater(0,a) ).

%------------------------------------------------------------------------------
