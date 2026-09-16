%------------------------------------------------------------------------------
% File     : ARI685_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Expand and rewrite polynomial
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : simplify0.pri [BHS07]
%          : poly_simplify0.p [Rue14]

% Status   : Theorem
% Rating   : 0.20 v9.3.0, 0.12 v9.1.0, 0.25 v9.0.0, 0.12 v8.2.0, 0.25 v7.5.0, 0.30 v7.4.0, 0.38 v7.3.0, 0.33 v7.0.0, 0.43 v6.4.0, 0.33 v6.3.0
% Syntax   : Number of formulae    :    6 (   2 unt;   4 typ;   0 def)
%            Number of atoms       :    2 (   2 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :   18 (   3 avg)
%            Number arithmetic     :   80 (   0 atm;  60 fun;  20 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :   12 (   4 usr;   9 con; 0-2 aty)
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

tff(d_type,type,
    d: $int ).

tff(eq,axiom,
    $sum($sum($sum($product(a,a),$product($product($sum(a,b),$sum($sum(c,d),1)),$sum(a,2))),b),$product(-1,$product($sum($sum($sum(a,b),c),d),$sum(2,c)))) = 0 ).

tff(conj,conjecture,
    $sum($product($product(d,b),a),$product(-1,$sum($sum($sum($sum($sum($sum($sum($sum($sum($sum($sum($difference($sum($product(-2,$product(a,a)),$product(-1,$product(c,a))),b),$product(-1,$product(b,a))),$product(2,c)),$product(-1,$product(c,b))),$product(c,c)),$product(-1,$product($product(c,a),a))),$product(-1,$product(2,$product(d,a)))),$product(-1,$product(2,$product(d,b)))),$product(-1,$product($product(c,b),a))),$product(d,c)),$product(-1,$product($product(d,a),a))),$product(2,d)))) = 0 ).

%------------------------------------------------------------------------------
