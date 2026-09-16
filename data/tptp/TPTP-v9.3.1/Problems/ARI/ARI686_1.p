%------------------------------------------------------------------------------
% File     : ARI686_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Expand and rewrite polynomial
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : simplify10.pri [BHS07]
%          : poly_simplify10.p [Rue14]

% Status   : Theorem
% Rating   : 0.20 v9.3.0, 0.38 v9.1.0, 0.50 v9.0.0, 0.38 v8.1.0, 0.50 v7.5.0, 0.60 v7.4.0, 0.62 v7.3.0, 0.50 v7.0.0, 0.57 v6.4.0, 1.00 v6.3.0
% Syntax   : Number of formulae    :    4 (   3 unt;   1 typ;   0 def)
%            Number of atoms       :    3 (   3 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :   21 (   4 avg)
%            Number arithmetic     :   93 (   0 atm;  69 fun;  24 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :   15 (   1 usr;  13 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
tff(a_type,type,
    a: $int ).

tff(eq1,axiom,
    $product($product(5,a),a) = $product(2,a) ).

tff(eq2,axiom,
    $product(a,$sum(a,$product(-1,$product($product(2,a),$sum(a,$product($product(3,a),$sum(a,$product(-1,$product($product(4,a),$sum(a,$product($product(5,a),$sum(a,$product(-1,$product($product(6,a),$sum(a,$product($product(7,a),$sum(a,$product(-1,$product($product(8,a),$sum(9,a)))))))))))))))))))) = 0 ).

tff(conj,conjecture,
    $sum($product(2,$product($product($product($product($product($product($product(a,a),a),a),a),a),a),a)),$product(-1,$sum($sum($sum($sum($sum($product(612,a),$product(-1,$product(a,a))),$product(-2,$product($product(a,a),a))),$product(2,$product($product($product($product(a,a),a),a),a))),$product(-2,$product($product($product($product($product(a,a),a),a),a),a))),$product(-2,$product($product($product($product($product($product(a,a),a),a),a),a),a))))) = 0 ).

%------------------------------------------------------------------------------
