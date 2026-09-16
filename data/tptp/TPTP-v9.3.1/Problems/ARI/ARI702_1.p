%------------------------------------------------------------------------------
% File     : ARI702_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Solve a simple system of nonlinear equations
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : simplify25.pri [BHS07]
%          : poly_simplify25.p [Rue14]

% Status   : Theorem
% Rating   : 0.00 v9.3.0, 0.12 v8.2.0, 0.25 v7.5.0, 0.30 v7.4.0, 0.25 v7.3.0, 0.17 v7.0.0, 0.43 v6.4.0, 0.33 v6.3.0
% Syntax   : Number of formulae    :    9 (   4 unt;   5 typ;   0 def)
%            Number of atoms       :    4 (   4 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :    3 (   1 avg)
%            Number arithmetic     :   11 (   0 atm;   7 fun;   4 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    8 (   5 usr;   7 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
tff(x_type,type,
    x: $int ).

tff(y_type,type,
    y: $int ).

tff(a_type,type,
    a: $int ).

tff(z_type,type,
    z: $int ).

tff(b_type,type,
    b: $int ).

tff(eq1,axiom,
    $product($product(2,x),y) = a ).

tff(eq2,axiom,
    $product($product(2,y),z) = b ).

tff(eq3,axiom,
    $product(a,z) = 2 ).

tff(conj,conjecture,
    $product($product(x,y),z) = 1 ).

%------------------------------------------------------------------------------
