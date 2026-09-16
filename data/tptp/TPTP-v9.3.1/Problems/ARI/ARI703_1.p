%------------------------------------------------------------------------------
% File     : ARI703_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Sum-of-squares decomposition
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : simplify26.pri [BHS07]
%          : poly_simplify26.p [Rue14]

% Status   : Theorem
% Rating   : 1.00 v6.3.0
% Syntax   : Number of formulae    :    8 (   1 unt;   7 typ;   0 def)
%            Number of atoms       :    1 (   1 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :    8 (   2 avg)
%            Number arithmetic     :   14 (   0 atm;  13 fun;   1 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :   10 (   7 usr;   8 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
%------------------------------------------------------------------------------
tff(x_type,type,
    x: $int ).

tff(y_type,type,
    y: $int ).

tff(z_type,type,
    z: $int ).

tff(t_type,type,
    t: $int ).

tff(u_type,type,
    u: $int ).

tff(v_type,type,
    v: $int ).

tff(w_type,type,
    w: $int ).

tff(eq,axiom,
    $sum($sum($sum($sum($sum($sum($product(x,x),$product(y,y)),$product(z,z)),$product(t,t)),$product(u,u)),$product(v,v)),$product(w,w)) = 1234567890987654321 ).

%------------------------------------------------------------------------------
