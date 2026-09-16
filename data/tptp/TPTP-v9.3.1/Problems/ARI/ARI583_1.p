%------------------------------------------------------------------------------
% File     : ARI583_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : Inequation system is solvable (choose, e.g., W = 3 - X)
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v7.4.0, 0.17 v7.3.0, 0.25 v7.1.0, 0.17 v7.0.0, 0.00 v6.1.0, 0.33 v6.0.0, 0.38 v5.4.0, 0.25 v5.3.0, 0.43 v5.2.0, 0.60 v5.1.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    7 (   0 equ)
%            Maximal formula atoms :    7 (   7 avg)
%            Number of connectives :    6 (   0   ~;   1   |;   4   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    9 (   9 avg)
%            Maximal term depth    :    3 (   1 avg)
%            Number arithmetic     :   19 (   7 atm;   3 fun;   5 num;   4 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    4 (   0 usr;   3 con; 0-2 aty)
%            Number of variables   :    4 (   3   !;   1   ?;   4   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(mix_quant_ineq_sys_solvable_4,conjecture,
    ! [X: $int,Y: $int,Z: $int] :
      ( ( $less(0,X)
        & $lesseq(0,Y)
        & $lesseq(0,Z)
        & ( $less(X,Y)
          | $less(X,Z) ) )
     => ? [W: $int] :
          ( $less($sum(X,W),4)
          & $less(3,$sum($sum(Y,Z),W)) ) ) ).

%------------------------------------------------------------------------------
