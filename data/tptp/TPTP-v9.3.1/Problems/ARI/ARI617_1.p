%------------------------------------------------------------------------------
% File     : ARI617_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : Two different definitions of absolute value agree
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v9.3.0, 0.12 v8.2.0, 0.25 v8.1.0, 0.12 v7.5.0, 0.20 v7.4.0, 0.00 v6.3.0, 0.14 v6.2.0, 0.50 v6.1.0, 0.56 v6.0.0, 0.57 v5.5.0, 0.56 v5.4.0, 0.62 v5.3.0, 0.70 v5.2.0, 0.83 v5.1.0
% Syntax   : Number of formulae    :    3 (   0 unt;   2 typ;   0 def)
%            Number of atoms       :    8 (   3 equ)
%            Maximal formula atoms :    8 (   8 avg)
%            Number of connectives :    7 (   0   ~;   2   |;   4   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    7 (   7 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :   12 (   5 atm;   3 fun;   1 num;   3 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    2 (   2   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    4 (   2 usr;   1 con; 0-1 aty)
%            Number of variables   :    3 (   3   !;   0   ?;   3   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(f_type,type,
    f: $int > $int ).

tff(g_type,type,
    g: $int > $int ).

tff(absolute_value_defs,conjecture,
    ( ( ! [X: $int] :
          ( $lesseq(X,f(X))
          & $lesseq($uminus(X),f(X))
          & ( $lesseq(f(X),X)
            | $lesseq(f(X),$uminus(X)) ) )
      & ! [X: $int] :
          ( $lesseq(0,g(X))
          & ( ( g(X) = X )
            | ( g(X) = $uminus(X) ) ) ) )
   => ! [X: $int] : ( f(X) = g(X) ) ) ).

%------------------------------------------------------------------------------
