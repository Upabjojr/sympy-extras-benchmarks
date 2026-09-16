%------------------------------------------------------------------------------
% File     : ARI609_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : For mon. f, 0<=a-b => b<=a => f(b)<=f(a) => 0<=f(a)-f(b)
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v7.3.0, 0.12 v7.1.0, 0.00 v6.2.0, 0.20 v6.1.0, 0.33 v6.0.0, 0.38 v5.4.0, 0.62 v5.3.0, 0.71 v5.2.0, 0.80 v5.1.0
% Syntax   : Number of formulae    :    4 (   0 unt;   3 typ;   0 def)
%            Number of atoms       :    4 (   0 equ)
%            Maximal formula atoms :    4 (   4 avg)
%            Number of connectives :    3 (   0   ~;   0   |;   1   &)
%                                         (   0 <=>;   2  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    6 (   6 avg)
%            Maximal term depth    :    4 (   2 avg)
%            Number arithmetic     :   12 (   4 atm;   4 fun;   2 num;   2 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    1 (   1   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    6 (   3 usr;   3 con; 0-2 aty)
%            Number of variables   :    2 (   2   !;   0   ?;   2   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(f_type,type,
    f: $int > $int ).

tff(a_type,type,
    a: $int ).

tff(b_type,type,
    b: $int ).

tff(f_mon_implies_f_a_b_1,conjecture,
    ( ( ! [X: $int,Y: $int] :
          ( $lesseq(X,Y)
         => $lesseq(f(X),f(Y)) )
      & $lesseq(0,$sum(a,$uminus(b))) )
   => $lesseq(0,$sum(f(a),$uminus(f(b)))) ) ).

%------------------------------------------------------------------------------
