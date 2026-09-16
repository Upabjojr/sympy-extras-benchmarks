%------------------------------------------------------------------------------
% File     : ARI588_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : If X = 2 then Y < X-1 xor 3-X <= Y
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v7.4.0, 0.17 v7.3.0, 0.38 v7.1.0, 0.17 v7.0.0, 0.00 v6.2.0, 0.40 v6.1.0, 0.56 v6.0.0, 0.62 v5.3.0, 0.86 v5.2.0, 1.00 v5.1.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    2 (   0 equ)
%            Maximal formula atoms :    2 (   2 avg)
%            Number of connectives :    2 (   1   ~;   0   |;   0   &)
%                                         (   1 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    5 (   5 avg)
%            Maximal term depth    :    3 (   1 avg)
%            Number arithmetic     :    9 (   2 atm;   3 fun;   2 num;   2 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    4 (   0 usr;   2 con; 0-2 aty)
%            Number of variables   :    2 (   1   !;   1   ?;   2   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(exists_X_complementary_halflines,conjecture,
    ? [X: $int] :
    ! [Y: $int] :
      ~ ( $less(Y,$sum(X,-1))
      <=> $lesseq($sum(3,$uminus(X)),Y) ) ).

%------------------------------------------------------------------------------
