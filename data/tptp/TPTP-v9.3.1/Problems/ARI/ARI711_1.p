%------------------------------------------------------------------------------
% File     : ARI711_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Expand the equation (a+b+c+1)^4 = 0
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : simplify8.pri [BHS07]
%          : poly_simplify8.p [Rue14]

% Status   : Theorem
% Rating   : 0.20 v9.3.0, 0.12 v9.1.0, 0.25 v9.0.0, 0.12 v8.2.0, 0.25 v7.5.0, 0.30 v7.4.0, 0.38 v7.3.0, 0.33 v7.0.0, 0.43 v6.4.0, 0.33 v6.3.0
% Syntax   : Number of formulae    :    5 (   2 unt;   3 typ;   0 def)
%            Number of atoms       :    2 (   2 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :   37 (   4 avg)
%            Number arithmetic     :  197 (   0 atm; 155 fun;  42 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :   14 (   3 usr;  11 con; 0-2 aty)
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

tff(eq,axiom,
    $product($product($product($sum($sum($sum(a,b),c),1),$sum($sum($sum(a,b),c),1)),$sum($sum($sum(a,b),c),1)),$sum($sum($sum(a,b),c),1)) = 0 ).

tff(conj,conjecture,
    $sum($product($product($product(c,c),c),c),$product(-1,$sum($sum($sum($sum($sum($sum($sum($sum($sum($sum($sum($sum($sum($sum($sum($sum($sum($sum($difference($sum($sum($sum($sum($sum($sum($sum($sum($sum($difference($sum($sum($sum($difference($product(-1,1),$product(4,a)),$product(-6,$product(a,a))),$product(-4,$product($product(a,a),a))),$product(-1,$product($product($product(a,a),a),a))),$product(4,b)),$product(-12,$product(b,a))),$product(-6,$product(b,b))),$product(-12,$product($product(b,a),a))),$product(-12,$product($product(b,b),a))),$product(-4,$product($product(b,b),b))),$product(-4,$product($product($product(b,a),a),a))),$product(-6,$product($product($product(b,b),a),a))),$product(-4,$product($product($product(b,b),b),a))),$product(-1,$product($product($product(b,b),b),b))),$product(4,c)),$product(-12,$product(c,a))),$product(-12,$product(c,b))),$product(-6,$product(c,c))),$product(-12,$product($product(c,a),a))),$product(-24,$product($product(c,b),a))),$product(-12,$product($product(c,b),b))),$product(-12,$product($product(c,c),a))),$product(-12,$product($product(c,c),b))),$product(-4,$product($product(c,c),c))),$product(-4,$product($product($product(c,a),a),a))),$product(-12,$product($product($product(c,b),a),a))),$product(-12,$product($product($product(c,b),b),a))),$product(-4,$product($product($product(c,b),b),b))),$product(-6,$product($product($product(c,c),a),a))),$product(-12,$product($product($product(c,c),b),a))),$product(-6,$product($product($product(c,c),b),b))),$product(-4,$product($product($product(c,c),c),a))),$product(-4,$product($product($product(c,c),c),b))))) = 0 ).

%------------------------------------------------------------------------------
