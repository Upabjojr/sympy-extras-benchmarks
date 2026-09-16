%------------------------------------------------------------------------------
% File     : ARI578_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : Inequation system is solvable (e.g., X = 3, Y = 6)
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v7.4.0, 0.17 v7.3.0, 0.25 v7.1.0, 0.17 v7.0.0, 0.00 v6.2.0, 0.40 v6.1.0, 0.33 v6.0.0, 0.38 v5.4.0, 0.25 v5.3.0, 0.43 v5.2.0, 0.60 v5.1.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    4 (   0 equ)
%            Maximal formula atoms :    4 (   4 avg)
%            Number of connectives :    3 (   0   ~;   0   |;   3   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    6 (   6 avg)
%            Maximal term depth    :    3 (   1 avg)
%            Number arithmetic     :   14 (   4 atm;   3 fun;   5 num;   2 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    5 (   0 usr;   3 con; 0-2 aty)
%            Number of variables   :    2 (   0   !;   2   ?;   2   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(ineq_sys_solvable_3,conjecture,
    ? [X: $int,Y: $int] :
      ( $lesseq(2,X)
      & $lesseq(2,Y)
      & $lesseq($sum(X,Y),9)
      & $lesseq(12,$sum($product(2,X),Y)) ) ).

%------------------------------------------------------------------------------
