%------------------------------------------------------------------------------
% File     : ARI699_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Nonlinear inequality reasoning
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : simplify22.pri [BHS07]
%          : poly_simplify22.p [Rue14]

% Status   : Unsatisfiable
% Rating   : 0.00 v9.1.0, 0.20 v9.0.0, 0.00 v8.2.0, 0.25 v8.1.0, 0.33 v7.3.0, 0.25 v7.1.0, 0.33 v7.0.0, 0.00 v6.4.0, 1.00 v6.3.0
% Syntax   : Number of formulae    :    7 (   4 unt;   3 typ;   0 def)
%            Number of atoms       :    4 (   1 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :    4 (   2 avg)
%            Number arithmetic     :   15 (   3 atm;   7 fun;   5 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    3 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    8 (   3 usr;   6 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_UNS_EQU_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
tff(z_type,type,
    z: $int ).

tff(x_type,type,
    x: $int ).

tff(y_type,type,
    y: $int ).

tff(ineq1,axiom,
    $greater(x,0) ).

tff(ineq2,axiom,
    $greater(y,0) ).

tff(ineq3,axiom,
    $lesseq(0,$sum($product($product(z,z),x),$product(-1,$product(y,x)))) ).

tff(eq,axiom,
    $product($product(2,z),z) = y ).

%------------------------------------------------------------------------------
