%------------------------------------------------------------------------------
% File     : ARI710_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Simple rewriting: b * 1 = a*c*d implies b = d*a*c
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : simplify7.pri [BHS07]
%          : poly_simplify7.p [Rue14]

% Status   : Theorem
% Rating   : 0.20 v9.3.0, 0.12 v8.2.0, 0.25 v7.5.0, 0.30 v7.4.0, 0.38 v7.3.0, 0.33 v7.0.0, 0.43 v6.4.0, 0.33 v6.3.0
% Syntax   : Number of formulae    :    6 (   2 unt;   4 typ;   0 def)
%            Number of atoms       :    2 (   2 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :    3 (   2 avg)
%            Number arithmetic     :    6 (   0 atm;   5 fun;   1 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    6 (   4 usr;   5 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
tff(b_type,type,
    b: $int ).

tff(a_type,type,
    a: $int ).

tff(c_type,type,
    c: $int ).

tff(d_type,type,
    d: $int ).

tff(eq,axiom,
    $product(b,1) = $product($product(a,c),d) ).

tff(conj,conjecture,
    b = $product($product(d,a),c) ).

%------------------------------------------------------------------------------
