%------------------------------------------------------------------------------
% File     : ARI618_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : Absolute value (unusually defined) is idempotent
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v9.3.0, 0.12 v8.2.0, 0.25 v7.5.0, 0.30 v7.4.0, 0.00 v6.3.0, 0.14 v6.2.0, 0.50 v6.1.0, 0.56 v6.0.0, 0.57 v5.5.0, 0.56 v5.4.0, 0.62 v5.3.0, 0.70 v5.2.0, 0.83 v5.1.0
% Syntax   : Number of formulae    :    2 (   0 unt;   1 typ;   0 def)
%            Number of atoms       :    5 (   1 equ)
%            Maximal formula atoms :    5 (   5 avg)
%            Number of connectives :    4 (   0   ~;   1   |;   2   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    6 (   6 avg)
%            Maximal term depth    :    3 (   2 avg)
%            Number arithmetic     :    8 (   4 atm;   2 fun;   0 num;   2 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    1 (   1   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    2 (   1 usr;   0 con; 1-1 aty)
%            Number of variables   :    2 (   2   !;   0   ?;   2   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(f_type,type,
    f: $int > $int ).

tff(absolute_value_idempotent,conjecture,
    ( ! [X: $int] :
        ( $lesseq(X,f(X))
        & $lesseq($uminus(X),f(X))
        & ( $lesseq(f(X),X)
          | $lesseq(f(X),$uminus(X)) ) )
   => ! [X: $int] : ( f(f(X)) = f(X) ) ) ).

%------------------------------------------------------------------------------
