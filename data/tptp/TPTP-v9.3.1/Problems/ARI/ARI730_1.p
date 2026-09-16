%------------------------------------------------------------------------------
% File     : ARI730_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : If X =< 7.2 and X is an integer, then X =< 7
% Version  : Especial.
% English  :

% Refs     : [Wal14] Waldmann (2014), Email to Geoff Sutcliffe
% Source   : [Wal14]
% Names    : 

% Status   : Theorem
% Rating   : 0.25 v9.1.0, 0.40 v9.0.0, 0.25 v8.2.0, 0.17 v7.5.0, 0.20 v7.4.0, 0.33 v7.3.0, 0.25 v7.1.0, 0.33 v6.3.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    3 (   0 equ)
%            Maximal formula atoms :    3 (   3 avg)
%            Number of connectives :    2 (   0   ~;   0   |;   1   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    4 (   4 avg)
%            Maximal term depth    :    1 (   1 avg)
%            Number arithmetic     :    6 (   3 atm;   0 fun;   2 num;   1 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 1-2 aty)
%            Number of functors    :    2 (   0 usr;   2 con; 0-0 aty)
%            Number of variables   :    1 (   1   !;   0   ?;   1   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments : 
%------------------------------------------------------------------------------
tff(prove,conjecture,
    ! [X: $real] :
      ( ( $is_int(X)
        & $lesseq(X,7.2) )
     => $lesseq(X,7.0) ) ).

%------------------------------------------------------------------------------
