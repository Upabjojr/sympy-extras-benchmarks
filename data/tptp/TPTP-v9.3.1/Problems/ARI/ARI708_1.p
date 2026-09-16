%------------------------------------------------------------------------------
% File     : ARI708_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Expand and rewrite polynomials
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : simplify5.pri [BHS07]
%          : poly_simplify5.p [Rue14]

% Status   : Theorem
% Rating   : 0.20 v9.3.0, 0.25 v8.2.0, 0.38 v7.5.0, 0.40 v7.4.0, 0.38 v7.3.0, 0.33 v7.0.0, 0.43 v6.4.0, 0.33 v6.3.0
% Syntax   : Number of formulae    :    7 (   3 unt;   4 typ;   0 def)
%            Number of atoms       :    3 (   3 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :    6 (   2 avg)
%            Number arithmetic     :   20 (   0 atm;  15 fun;   5 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :   10 (   4 usr;   7 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
tff(a_type,type,
    a: $int ).

tff(c_type,type,
    c: $int ).

tff(d_type,type,
    d: $int ).

tff(b_type,type,
    b: $int ).

tff(eq1,axiom,
    $sum(a,$product(-1,$product($sum(c,d),$sum(d,c)))) = 0 ).

tff(eq2,axiom,
    $product($difference(c,d),$difference(c,d)) = b ).

tff(conj,conjecture,
    $sum($sum(a,b),$product(-1,$product(2,$sum($product(c,c),$product(d,d))))) = 0 ).

%------------------------------------------------------------------------------
