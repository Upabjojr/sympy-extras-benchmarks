%------------------------------------------------------------------------------
% File     : ARI341_1 : TPTP v9.3.1. Released v5.0.0.
% Domain   : Arithmetic
% Problem  : Rational: -2/5 * (145/2 - 569/5) less than (- 76/25) + 271/10
% Version  : Especial.
% English  :

% Refs     :
% Source   : [TPTP]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v8.2.0, 0.17 v7.5.0, 0.20 v7.4.0, 0.17 v7.3.0, 0.12 v7.1.0, 0.17 v7.0.0, 0.00 v6.3.0, 0.25 v6.2.0, 0.60 v6.1.0, 0.44 v6.0.0, 0.38 v5.3.0, 0.29 v5.2.0, 0.20 v5.1.0, 0.25 v5.0.0
% Syntax   : Number of formulae    :    2 (   1 unt;   1 typ;   0 def)
%            Number of atoms       :    1 (   0 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :    3 (   2 avg)
%            Number arithmetic     :   10 (   1 atm;   4 fun;   5 num;   0 var)
%            Number of types       :    2 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    1 (   1   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   1 usr;   0 prp; 1-2 aty)
%            Number of functors    :    9 (   0 usr;   5 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(p_type,type,
    p: $rat > $o ).

tff(rat_combined_problem_7,conjecture,
    $less($product(-2/5,$difference(145/2,569/5)),$sum($uminus(76/25),271/10)) ).

%------------------------------------------------------------------------------
