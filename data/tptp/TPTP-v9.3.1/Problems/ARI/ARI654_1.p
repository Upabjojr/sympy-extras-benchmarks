%------------------------------------------------------------------------------
% File     : ARI654_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : y >= 5*x - 1, y <= 5*x, 5*z <= y - 1, 5*z >= y - 2 are unsat
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : inequations3.pri [BHS07]
%          : inequations3.p [Rue14]

% Status   : Unsatisfiable
% Rating   : 0.00 v6.3.0
% Syntax   : Number of formulae    :    7 (   4 unt;   3 typ;   0 def)
%            Number of atoms       :    4 (   0 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :    3 (   1 avg)
%            Number arithmetic     :   18 (   4 atm;   7 fun;   7 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    8 (   3 usr;   6 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_UNS_NEQ_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
tff(x_type,type,
    x: $int ).

tff(y_type,type,
    y: $int ).

tff(z_type,type,
    z: $int ).

tff(conj,axiom,
    $greatereq(y,$difference($product(5,x),1)) ).

tff(conj_001,axiom,
    $lesseq(y,$product(5,x)) ).

tff(conj_002,axiom,
    $lesseq($product(5,z),$difference(y,1)) ).

tff(conj_003,axiom,
    $greatereq($product(5,z),$difference(y,2)) ).

%------------------------------------------------------------------------------
