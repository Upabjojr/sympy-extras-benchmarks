%------------------------------------------------------------------------------
% File     : ARI689_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Rewrite polynomial using linear equations
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : simplify13.pri [BHS07]
%          : poly_simplify13.p [Rue14]

% Status   : Theorem
% Rating   : 0.20 v9.3.0, 0.25 v9.1.0, 0.38 v9.0.0, 0.25 v8.2.0, 0.38 v7.5.0, 0.40 v7.4.0, 0.38 v7.3.0, 0.33 v7.0.0, 0.43 v6.4.0, 0.33 v6.3.0
% Syntax   : Number of formulae    :    7 (   3 unt;   4 typ;   0 def)
%            Number of atoms       :    3 (   3 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :    8 (   2 avg)
%            Number arithmetic     :   26 (   0 atm;  18 fun;   8 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :   14 (   4 usr;  12 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
tff(y_type,type,
    y: $int ).

tff(a_type,type,
    a: $int ).

tff(x_type,type,
    x: $int ).

tff(b_type,type,
    b: $int ).

tff(eq1,axiom,
    $product(98164184,y) = a ).

tff(eq2,axiom,
    $product(6472,x) = b ).

tff(conj,conjecture,
    $sum($product(1,$product($product(y,x),b)),$product(-1,$sum($sum($product(166,$product($product(x,b),a)),$product(2427,$product($product(x,x),a))),$product(-2523496,$product($product(y,b),b))))) = 0 ).

%------------------------------------------------------------------------------
