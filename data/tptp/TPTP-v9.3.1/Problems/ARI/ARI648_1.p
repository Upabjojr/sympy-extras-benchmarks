%------------------------------------------------------------------------------
% File     : ARI648_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : 2*a > 0 | -4*b + 2*a < 8 implies a >= 1 | a-2*b<=3 | 20*a-30*b=7
% Version  : Especial.
% English  :

% Refs     : [BHS07] Beckert et al. (2007), Verification of Object-Oriented
%          : [Rue14] Ruemmer (2014), Email to Geoff Sutcliffe
% Source   : [Rue14]
% Names    : simplify4.pri [BHS07]
%          : ineqs_simplify4.p [Rue14]

% Status   : Theorem
% Rating   : 0.00 v9.3.0, 0.12 v9.1.0, 0.25 v9.0.0, 0.12 v7.5.0, 0.10 v7.4.0, 0.00 v6.3.0
% Syntax   : Number of formulae    :    4 (   0 unt;   2 typ;   0 def)
%            Number of atoms       :    5 (   1 equ)
%            Maximal formula atoms :    3 (   2 avg)
%            Number of connectives :    3 (   0   ~;   3   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    3 (   3 avg)
%            Maximal term depth    :    4 (   2 avg)
%            Number arithmetic     :   28 (   4 atm;  11 fun;  13 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    5 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :   15 (   2 usr;  12 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : KeY arithmetic regression test, http://www.key-project.org
%------------------------------------------------------------------------------
tff(b_type,type,
    b: $int ).

tff(a_type,type,
    a: $int ).

tff(conj,axiom,
    ( $greater(8,$difference($product(2,a),$product(4,b)))
    | $less(0,$product(2,a)) ) ).

tff(conj_001,conjecture,
    ( ( $sum($product(20,a),$product(-1,$product(30,b))) = 7 )
    | $greatereq(3,$sum(a,$product(-1,$product(2,b))))
    | $lesseq(1,a) ) ).

%------------------------------------------------------------------------------
